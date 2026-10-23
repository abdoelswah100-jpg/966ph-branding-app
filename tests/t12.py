import json, os, base64, re, zipfile, io
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'; S9 = W + 's9/'; OUT = W + 's12/'; os.makedirs(OUT, exist_ok=True)
DATA = open(W + 'out4/966-data-v1.json', encoding='utf-8').read()
URL = 'file://' + W + 'full28.html'
errs, res = [], {}
AR = re.compile(r'[ء-ي][ء-ي ]*')
def b64(pg, expr):
    return base64.b64decode(pg.evaluate("async()=>{const b=await (" + expr + ");const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)}"))
MOCK = r"""
window.__calls=[];window.__files={};window.__bio=(()=>{try{return JSON.parse(localStorage.getItem('__bio'))||{avail:true,ok:true}}catch(e){return{avail:true,ok:true}}})();
window.Capacitor={isNativePlatform:()=>true,Plugins:{
 Filesystem:{mkdir:async o=>{},writeFile:async o=>{__files[o.path]=1;return{uri:'file:///x/'+o.path}},readdir:async o=>({files:[]}),deleteFile:async o=>{}},
 Share:{share:async o=>{__calls.push(['share'])}},
 App:{addListener:(e,f)=>{window.__back=f},exitApp:()=>{__calls.push(['exit'])}},
 NativeBiometric:{isAvailable:async()=>({isAvailable:__bio.avail}),verifyIdentity:async o=>{__calls.push(['bio',o.reason]);if(!__bio.ok)throw new Error('fail')}}}};
"""
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, device_scale_factor=2, accept_downloads=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    dl = []; pg.on('dialog', lambda x: (dl.append(x.message[:90]), x.accept()))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>localStorage.setItem('ads',d)", DATA); pg.reload(); pg.wait_for_timeout(2200)
    res['ver'] = pg.evaluate("VER")
    # --- migration: Health Room removed, snapshot taken ---
    res['hr_left'] = pg.evaluate("DB.ph.reduce((a,p)=>a+((p.rows.al||[]).filter(r=>r.sec=='Health Room').length),0)")
    res['hr_snap'] = pg.evaluate("SNAPS.map(x=>x.why)")
    res['hr_ls'] = pg.evaluate("(localStorage.getItem('ads')||'').includes('\"Health Room\"')")
    res['al_name'] = pg.evaluate("[T.find(t=>t.id=='al').n,SZ('mt.al')]")
    # --- totals 1533 ---
    pid = pg.evaluate("DB.ph.find(p=>p.no=='1533').id")
    pg.evaluate(f"V={{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(300)
    res['sum_ttot'] = pg.evaluate("[...document.querySelectorAll('#rp .ttot')].map(x=>x.innerText.replace(/\\s+/g,' '))")
    res['sum_tsum'] = pg.evaluate("[...document.querySelectorAll('#rp table.tsum tr')].map(r=>[...r.cells].map(c=>c.innerText).join(' | '))")
    res['sum_check'] = pg.evaluate("""(()=>{const p=DB.ph.find(x=>x.no=='1533');let ok=[];TY(p).forEach(t=>{const rs=p.rows[t.id]||[];if(!rs.length||t.id=='ws'||t.id=='wh'||t.id=='eg'||t.id=='md'||t.id=='al'||t.auto)return;const q=rs.reduce((a,r)=>a+(+r.q||0),0);ok.push(t.id+':'+(tTot(t,rs)==q+' قطعة'))});return ok})()""")
    y = pg.evaluate("(()=>{const h=[...document.querySelectorAll('#rp h3')].find(h=>/Floor Header/.test(h.textContent));return h.getBoundingClientRect().top+scrollY-120})()")
    pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(150); pg.screenshot(path=OUT + '01_sum_wh_total.png')
    pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(100); pg.screenshot(path=OUT + '01b_sum_top.png')
    open(OUT + 'sum1533.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    # summary Excel
    x = b64(pg, 'Promise.resolve(rpXlsx())'); open(OUT + 'sum1533.xlsx', 'wb').write(x)
    z = zipfile.ZipFile(io.BytesIO(x)); wb = z.read('xl/workbook.xml').decode(); s1 = z.read('xl/worksheets/sheet1.xml').decode()
    res['xlsx'] = {'sheets': re.findall(r'<sheet name="([^"]+)"', wb), 'pane': re.findall(r'<pane[^>]*/>', s1), 'tot_rows': len(re.findall(r's="3"', s1)), 'hdr': len(re.findall(r's="1"', s1)), 'rtl': 'rightToLeft="1"' in s1}
    # mgmt
    pg.click('button[data-sm="mgmt"]'); pg.wait_for_timeout(250)
    res['mgmt_tot'] = pg.evaluate("[...document.querySelectorAll('#rp tr.tot')].map(r=>r.innerText.replace(/\\s+/g,' ').trim())")
    pg.screenshot(path=OUT + '02_mgmt.png', full_page=True)
    x = b64(pg, 'Promise.resolve(rpXlsx())'); z = zipfile.ZipFile(io.BytesIO(x)); res['mgmt_xlsx_sheets'] = re.findall(r'<sheet name="([^"]+)"', z.read('xl/workbook.xml').decode())
    # delete a row in edit mode -> total updates
    pg.click('#edt'); pg.wait_for_timeout(150)
    before = pg.evaluate("[...document.querySelectorAll('#rp tr.tot')].map(r=>r.innerText.replace(/\\s+/g,' ').trim()).find(t=>/Wall Header/.test(t))")
    pg.evaluate("(()=>{const r=[...document.querySelectorAll('#rp tr')].find(r=>/^Wall Header/.test(r.cells[0]&&r.cells[0].innerText)&&r.querySelector('[data-rdel]'));r.querySelector('[data-rdel]').click()})()"); pg.wait_for_timeout(250)
    after = pg.evaluate("[...document.querySelectorAll('#rp tr.tot')].map(r=>r.innerText.replace(/\\s+/g,' ').trim()).find(t=>/Wall Header/.test(t))")
    res['mgmt_del'] = [before, after]
    pg.evaluate(f"(()=>{{const p=DB.ph.find(x=>x.id=={pid});p.rh=[];sv()}})()")
    # review cards
    pg.evaluate(f"V={{v:'rev',rv:{{ids:[{pid}],i:0}},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(250)
    res['rev_ttl'] = pg.evaluate("[...document.querySelectorAll('.icard.ttl')].map(x=>x.innerText.replace(/\\s+/g,' ').trim())")
    pg.screenshot(path=OUT + '03_review.png', full_page=False)
    # --- acrylic letters form ---
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{al:true}},dr:{{}},fo:{{al:1}},q:V.q}};render()"); pg.wait_for_timeout(200)
    def setsec(v):
        pg.select_option('select[data-t="al"][data-k="sec"]', v); pg.wait_for_timeout(150)
    def typ(k, v):
        pg.fill(f'input[data-t="al"][data-k="{k}"]', str(v)); pg.wait_for_timeout(80)
    def wval(): return pg.input_value('input[data-t="al"][data-k="w"]')
    out = {}
    for sec, lh in [('Health', 45), ('Baby', 45), ('Mizan', 55), ('Pharmacy', 50), ('Beauty', 45), ('Personal', 45), ('برسلات (Parcelat)', 21), ('Stay Healthy (خليك صحي)', 20), ('Health Room – Inside (داخلي)', 28), ('Health Room – Outside (خارجي)', 35)]:
        setsec(sec); typ('lh', lh); out[sec] = wval()
    setsec('Health'); typ('lh', 90); out['Health x2'] = wval()
    res['ratio'] = out
    res['al_opts'] = pg.evaluate("[...document.querySelector('select[data-t=\"al\"][data-k=\"sec\"]').options].map(o=>o.value)")
    typ('w', 333); res['manual'] = [wval(), pg.locator('button[data-ratr]').count()]
    pg.click('button[data-ratr]'); pg.wait_for_timeout(150); res['back_ratio'] = [wval(), pg.locator('small.autot').count()]
    pg.screenshot(path=OUT + '04_al_form.png')
    # add Health Room Inside -> 5 pieces
    n0 = pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.al.length")
    setsec('Health Room – Inside (داخلي)'); typ('lh', 28); typ('h', 60)
    pg.click('button[data-add="al"]'); pg.wait_for_timeout(250)
    res['hri_add'] = pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.al.slice({n0}).map(r=>[r.sec,r.lh,r.w,r.q,!!r.pc])")
    setsec('Health Room – Inside (داخلي)'); typ('lh', 28); typ('h', 60); pg.click('button[data-add="al"]'); pg.wait_for_timeout(250)
    res['hri_add2_pieces'] = pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.al.filter(r=>r.pc).length")
    # edit old row (Health w=400) keeps manual
    i = pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.al.findIndex(r=>r.sec=='Health'&&r.w==400)")
    pg.click(f'button[data-ed="al:{i}"]'); pg.wait_for_timeout(200); res['edit_old'] = [wval(), pg.locator('button[data-ratr]').count()]
    pg.click('button[data-ced]'); pg.wait_for_timeout(100)
    pg.evaluate(f"V={{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(200)
    res['al_total'] = pg.evaluate("[...document.querySelectorAll('#rp .ttot')].map(x=>x.innerText.replace(/\\s+/g,' ')).filter(t=>/Acrylic letters/.test(t))")
    # --- ratio bulk view ---
    pg.evaluate("V={v:'set',op:{},dr:{},q:V.q};render()"); pg.click('button[data-rto]'); pg.wait_for_timeout(200)
    res['rto_n'] = pg.evaluate("rtoRows().length"); pg.screenshot(path=OUT + '05_rto.png', full_page=True)
    pg.locator('input[data-rx]').first.uncheck(); pg.wait_for_timeout(150)
    w0 = pg.evaluate("DB.ph.map(p=>(p.rows.al||[]).map(r=>r.w)).flat().join(',')")
    pg.click('button[data-rxgo]'); pg.wait_for_timeout(300)
    res['rto_after'] = pg.evaluate("rtoRows().length")
    pg.click('button[data-undo]'); pg.wait_for_timeout(300)
    res['rto_undo_same'] = pg.evaluate("DB.ph.map(p=>(p.rows.al||[]).map(r=>r.w)).flat().join(',')") == w0
    # --- photos ---
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{__pho:true}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(200)
    pg.evaluate("V.phs='b'"); pg.set_input_files('#phin', [S9 + 'PH-652 plan.jpg', S9 + 'PH-652 plan.jpg']); pg.wait_for_timeout(2500)
    pg.evaluate("V.phs='a'"); pg.set_input_files('#phin', [S9 + 'PH-652 plan.jpg'] * 3); pg.wait_for_timeout(3000)
    res['pho_meta'] = pg.evaluate(f"(()=>{{const p=DB.ph.find(x=>x.id=={pid});return [phoList(p,'b').length,phoList(p,'a').length,phoList(p,'a')[0].sz]}})()")
    pg.reload(); pg.wait_for_timeout(2200)
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{__pho:true}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(800)
    res['pho_after_reload'] = pg.evaluate("[...document.querySelectorAll('img[data-pho]')].filter(i=>i.naturalWidth>0).length")
    y = pg.evaluate("document.querySelector('details[data-id=\"__pho\"]').getBoundingClientRect().top+scrollY-80"); pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT + '06_photos.png')
    pg.locator('button[data-phov]').first.click(); pg.wait_for_timeout(400); res['pho_zoom'] = pg.evaluate("(document.querySelector('.ovl.pov img')||{}).naturalWidth||0"); pg.screenshot(path=OUT + '06b_zoom.png'); pg.click('button[data-ovlx]')
    pg.locator('button[data-phdel^="a:"]').first.click(); pg.wait_for_timeout(250)
    res['pho_del'] = pg.evaluate(f"phoList(DB.ph.find(x=>x.id=={pid}),'a').length")
    pg.click('button[data-undo]'); pg.wait_for_timeout(300)
    res['pho_undo'] = pg.evaluate(f"phoList(DB.ph.find(x=>x.id=={pid}),'a').length")
    # warning
    p809 = pg.evaluate("DB.ph.find(p=>p.no=='809').id")
    pg.evaluate(f"(()=>{{const p=DB.ph.find(x=>x.id=={p809});p.st='مكتملة';V={{v:'ph',p:{p809},op:{{}},dr:{{}},q:V.q}};render()}})()"); pg.wait_for_timeout(200)
    res['warn_ph'] = pg.locator('.ywarn').count()
    pg.evaluate(f"V={{v:'rev',rv:{{ids:[{p809}],i:0}},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(200)
    res['warn_rev'] = pg.locator('.ywarn').count()
    pg.evaluate(f"V={{v:'sum',sm:'print',p:{p809},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(200)
    res['warn_in_sum'] = pg.locator('#rp .ywarn').count()
    # backup tab
    pg.evaluate("V={v:'bk',op:{},dr:{},q:V.q};render()"); pg.wait_for_timeout(200)
    pg.evaluate("document.querySelector('details.wsv').open=true"); pg.wait_for_timeout(100)
    res['wsv'] = pg.evaluate("[...document.querySelectorAll('details.wsv tr')].map(r=>r.innerText.replace(/\\s+/g,' '))")
    pg.screenshot(path=OUT + '07_bk.png', full_page=True)
    # full backup with photos
    with pg.expect_download() as d:
        pg.evaluate("window.showSaveFilePicker=undefined;navigator.canShare=()=>false"); pg.click('button[data-bkpf]')
    d.value.save_as(OUT + 'bkf.json'); j = json.load(open(OUT + 'bkf.json', encoding='utf-8'))
    res['bkf_photos'] = len(j.get('_photos', {})); res['bkf_has_lock'] = 'lk966' in json.dumps(j)
    with pg.expect_download() as d:
        pg.click('button[data-bkp]')
    d.value.save_as(OUT + 'bk.json'); j2 = json.load(open(OUT + 'bk.json', encoding='utf-8')); res['bk_photos'] = '_photos' in j2
    # spec export / import
    with pg.expect_download() as d:
        pg.click('button[data-spec]')
    d.value.save_as(OUT + 'spec.json'); sp = json.load(open(OUT + 'spec.json', encoding='utf-8'))
    sp['sizesAndMaterials']['wh.len']['value'] = ['100', '80', '50', '30']; sp['sizesAndMaterials']['wh.len']['changed'] = True
    sp['customAdTypes'] = ['Test type X']; json.dump(sp, open(OUT + 'spec2.json', 'w', encoding='utf-8'), ensure_ascii=False)
    pg.set_input_files('#specin', OUT + 'spec2.json'); pg.wait_for_timeout(500)
    res['spec_import'] = pg.evaluate("[JSON.stringify(SZ('wh.len')),DB.cfg.adTypes.includes('Test type X'),SNAPS[0].why]")
    open(OUT + 'bad.json', 'w').write('{"x":1}'); n_before = pg.evaluate("JSON.stringify(DB).length")
    pg.set_input_files('#specin', OUT + 'bad.json'); pg.wait_for_timeout(400)
    res['spec_bad_unchanged'] = pg.evaluate("JSON.stringify(DB).length") == n_before
    # restore full backup in a new context -> photos back
    ctx2 = br.new_context(viewport={'width': 400, 'height': 860}); p2 = ctx2.new_page(); p2.on('dialog', lambda x: x.accept()); p2.on('pageerror', lambda e: errs.append('P2 ' + str(e)))
    p2.goto(URL); p2.wait_for_timeout(1500); p2.click('button[data-tab="bk"]'); p2.wait_for_timeout(200)
    p2.set_input_files('#rst', OUT + 'bkf.json'); p2.wait_for_timeout(3000)
    res['restore_photos'] = p2.evaluate(f"Promise.all(['b','a'].flatMap(sl=>phoList(DB.ph.find(x=>x.id=={pid}),sl).map(x=>idbGet(phoKey({pid},sl,x.k))))).then(a=>a.filter(Boolean).length)")
    ctx2.close()
    # home card height + laptop has no lock
    pg.evaluate("V={v:'home',op:{},dr:{},q:{t:'',st:'',mo:''}};render()"); pg.wait_for_timeout(200)
    res['card_h'] = pg.evaluate("[...document.querySelectorAll('.pcard')].map(e=>Math.round(e.getBoundingClientRect().height))")
    res['home_overflow'] = pg.evaluate("document.documentElement.scrollWidth-innerWidth")
    pg.screenshot(path=OUT + '08_home.png')
    pg.evaluate("V={v:'gen',op:{},dr:{},q:V.q};render()"); res['laptop_lock_ui'] = pg.locator('button[data-lks]').count() + pg.locator('#lock').count()
    # English on new screens
    left = {}
    for name, js in [('sum', f"V={{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}}"), ('mgmt', f"V={{v:'sum',sm:'mgmt',p:{pid},op:{{}},dr:{{}},q:V.q}}"), ('ph', f"V={{v:'ph',p:{pid},op:{{__pho:true,al:true}},dr:{{}},fo:{{al:1}},q:V.q}}"), ('bk', "V={v:'bk',op:{},dr:{},q:V.q}"), ('rto', "V={v:'rto',op:{},dr:{},q:V.q,rx:{}}")]:
        pg.evaluate(f"DB.cfg.lang='en';{js};render();cfg()"); pg.wait_for_timeout(250)
        if name == 'bk': pg.evaluate("document.querySelector('details.wsv').open=true")
        t = pg.evaluate("document.body.innerText"); left[name] = sorted(set(x.strip() for x in AR.findall(t) if x.strip()))
        pg.screenshot(path=OUT + f'09_en_{name}.png', full_page=True)
    res['en_left'] = left
    pg.evaluate("DB.cfg.lang='';cfg();render()")
    res['dialogs'] = dl[-12:]
    ctx.close()

    # ================= Android lock =================
    ctx3 = br.new_context(viewport={'width': 400, 'height': 860}); ctx3.add_init_script(MOCK)
    a = ctx3.new_page(); a.on('pageerror', lambda e: errs.append('AND ' + str(e))); ad = []; a.on('dialog', lambda x: (ad.append(x.message[:80]), x.accept()))
    a.goto(URL); a.wait_for_timeout(300); a.evaluate("d=>localStorage.setItem('ads',d)", DATA); a.reload(); a.wait_for_timeout(3000)
    L = {}
    L['no_lock_first'] = a.locator('#lock').count()
    a.evaluate("V={v:'gen',op:{},dr:{},q:V.q};render()"); a.wait_for_timeout(200); a.screenshot(path=OUT + '10_gen_android.png')
    a.click('button[data-lks]'); a.wait_for_timeout(400); a.screenshot(path=OUT + '11_lockset.png', full_page=True)
    L['bioav'] = a.inner_text('#bioav')
    a.fill('#lks1', '1234'); a.fill('#lks2', '1234'); a.fill('#lksq', 'اسم أول مدرسة؟'); a.fill('#lksa', 'النهضة')
    a.click('button[data-lkon]'); a.wait_for_timeout(400)
    st = a.evaluate("JSON.parse(localStorage.getItem('lk966'))"); L['stored'] = {k: (v if k in ('on', 'mode', 'q') else ('hash' if isinstance(v, str) and len(v) == 64 else type(v).__name__)) for k, v in st.items()}
    L['pin_plain'] = '1234' in json.dumps(st) or 'النهضة' in json.dumps(st)
    L['in_db'] = 'lk966' in a.evaluate("JSON.stringify(DB)")
    # restart -> lock + bio
    a.reload(); a.wait_for_timeout(600); L['lock_shown'] = a.locator('#lock').count(); a.wait_for_timeout(1400); a.screenshot(path=OUT + '12_lock.png')
    a.wait_for_timeout(800); L['bio_unlocked'] = a.locator('#lock').count() == 0; L['bio_calls'] = a.evaluate("__calls.filter(c=>c[0]=='bio').length")
    # bio fails -> PIN
    a.evaluate("localStorage.setItem('__bio',JSON.stringify({avail:true,ok:false}))"); a.reload(); a.wait_for_timeout(3000); L['bio_fail_still_locked'] = a.locator('#lock').count(); a.screenshot(path=OUT + '12_lock.png')
    a.fill('#lkp', '9999'); a.click('button[data-lkpin]'); a.wait_for_timeout(300); L['wrong_msg'] = a.inner_text('#lkm')
    a.fill('#lkp', '1234'); a.click('button[data-lkpin]'); a.wait_for_timeout(300); L['pin_ok'] = a.locator('#lock').count() == 0
    # 5 wrong -> wait
    a.reload(); a.wait_for_timeout(3000)
    for _ in range(5):
        a.fill('#lkp', '0000'); a.click('button[data-lkpin]'); a.wait_for_timeout(200)
    L['after5'] = a.inner_text('#lkm')
    a.fill('#lkp', '1234'); a.click('button[data-lkpin]'); a.wait_for_timeout(300); L['blocked_even_right'] = a.locator('#lock').count()
    a.evaluate("(()=>{const L=JSON.parse(localStorage.getItem('lk966'));L.u=0;localStorage.setItem('lk966',JSON.stringify(L))})()")
    # forgot
    a.click('button[data-lkm="forgot"]'); a.wait_for_timeout(200); a.screenshot(path=OUT + '13_forgot.png')
    a.fill('#lka', 'غلط'); a.fill('#lkn1', '5678'); a.fill('#lkn2', '5678'); a.click('button[data-lkfa]'); a.wait_for_timeout(300); L['forgot_wrong'] = a.inner_text('#lkm')
    a.fill('#lka', ' النهضه '); a.fill('#lkn1', '5678'); a.fill('#lkn2', '5678'); a.click('button[data-lkfa]'); a.wait_for_timeout(400)
    L['forgot_ok'] = a.locator('#lock').count() == 0; L['data_kept'] = a.evaluate("DB.ph.length")
    # back button on lock exits
    a.reload(); a.wait_for_timeout(2500); a.evaluate("__back()"); L['back_exit'] = a.evaluate("__calls.some(c=>c[0]=='exit')")
    a.fill('#lkp', '5678'); a.click('button[data-lkpin]'); a.wait_for_timeout(300)
    # pin-only mode, then turn off
    a.evaluate("V={v:'lockset',from:'gen',op:{},dr:{},q:V.q};render()"); a.wait_for_timeout(300)
    a.fill('#lksc', '5678'); a.click('button[data-lkmd="pin"]'); a.click('button[data-lksv]'); a.wait_for_timeout(300)
    L['mode_pin'] = a.evaluate("JSON.parse(localStorage.getItem('lk966')).mode")
    a.reload(); a.wait_for_timeout(3000); L['pin_mode_no_bio_btn'] = a.locator('button[data-lkbio]').count()
    a.fill('#lkp', '5678'); a.click('button[data-lkpin]'); a.wait_for_timeout(300)
    a.evaluate("V={v:'lockset',from:'gen',op:{},dr:{},q:V.q};render()"); a.wait_for_timeout(300)
    a.fill('#lksc', '0000'); a.click('button[data-lkoff]'); a.wait_for_timeout(200); L['off_wrong_still_on'] = a.evaluate("!!JSON.parse(localStorage.getItem('lk966')).on")
    a.fill('#lksc', '5678'); a.click('button[data-lkoff]'); a.wait_for_timeout(300); L['off'] = a.evaluate("localStorage.getItem('lk966')")
    a.reload(); a.wait_for_timeout(2500); L['no_lock_after_off'] = a.locator('#lock').count()
    # device without biometrics -> falls back to pin
    a.evaluate("__bio.avail=false;V={v:'lockset',from:'gen',op:{},dr:{},q:V.q};render()"); a.wait_for_timeout(300)
    a.fill('#lks1', '2468'); a.fill('#lks2', '2468'); a.fill('#lksq', 'س'); a.fill('#lksa', 'جواب'); a.click('button[data-lkon]'); a.wait_for_timeout(400)
    L['nobio_mode'] = a.evaluate("JSON.parse(localStorage.getItem('lk966')).mode")
    L['dialogs'] = ad
    res['lock'] = L
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('\n'.join(errs) or 'NO ERRORS')

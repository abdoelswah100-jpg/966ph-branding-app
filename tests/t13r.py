import json, os, base64, re, zipfile, io
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'; OUT = W + 's13/'; os.makedirs(OUT, exist_ok=True)
d = json.load(open(W + 'out5/966-data-v1.1.json', encoding='utf-8'))
p1533 = [p for p in d['ph'] if p['no'] == '1533'][0]
for r in p1533['rows']['wh'][:3]: r['ck'] = True          # old ticks -> must become r=q
p1533['rows']['fh'][1]['ck'] = False
DATA = json.dumps(d, ensure_ascii=False)
URL = 'file://' + W + 'full28.html'
errs, res = [], {}
AR = re.compile(r'[ء-ي][ء-ي ]*')
def b64(pg, expr):
    return base64.b64decode(pg.evaluate("async()=>{const b=await (" + expr + ");const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)}"))
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, device_scale_factor=2, accept_downloads=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    dl = []; pg.on('dialog', lambda x: (dl.append(x.message[:90]), x.accept()))
    toasts = []
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>localStorage.setItem('ads',d)", DATA); pg.reload(); pg.wait_for_timeout(2200)
    res['ver'] = pg.evaluate('VER')
    pid = pg.evaluate("DB.ph.find(p=>p.no=='1533').id")
    P = f"DB.ph.find(p=>p.id=={pid})"
    # ---- migration ----
    res['mig'] = pg.evaluate(f"(()=>{{const p={P};return [p.rows.wh.slice(0,3).map(r=>[r.q,r.r,'ck' in r]),[p.rows.fh[1].r,'ck' in p.rows.fh[1]],SNAPS.map(x=>x.why)]}})()")
    res['ck_left'] = pg.evaluate("DB.ph.some(p=>Object.values(p.rows).some(a=>Array.isArray(a)&&a.some(r=>'ck' in r)))")
    # approve review -> fingerprint must not change with r/x
    pg.evaluate(f"(()=>{{const p={P};p.rev=true;p.revFp=fp(p);sv()}})()")
    fp0 = pg.evaluate(f"fp({P})")
    # ---- checklist (receipt by count) ----
    pg.evaluate(f"V={{v:'rcv',rn:String({P}.no),p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(250)
    res['ck_groups'] = pg.evaluate("[...document.querySelectorAll('main h3.tkh span')].map(x=>x.textContent)")
    pg.screenshot(path=OUT + '01_checklist.png', full_page=False)
    i_fh = pg.evaluate(f"{P}.rows.fh.findIndex(r=>+r.q>=3)")
    q_fh = pg.evaluate(f"{P}.rows.fh[{i_fh}].q")
    pg.click(f'button[data-tk="r:fh:{i_fh}:1"]'); pg.click(f'button[data-tk="r:fh:{i_fh}:1"]'); pg.wait_for_timeout(150)
    res['r_plus2'] = pg.evaluate(f"{P}.rows.fh[{i_fh}].r")
    pg.fill(f'input[data-tv="r:fh:{i_fh}"]', '1'); pg.dispatch_event(f'input[data-tv="r:fh:{i_fh}"]', 'change'); pg.wait_for_timeout(150)
    res['r_typed'] = pg.evaluate(f"{P}.rows.fh[{i_fh}].r")
    res['row_partial']=pg.evaluate(f"document.querySelector('input[data-tv=\"r:fh:{i_fh}\"]').closest('tr').className")
    pg.click(f'button[data-tf="r:ec:0"]'); pg.wait_for_timeout(150)
    res['r_tick_ec0'] = pg.evaluate(f"[{P}.rows.ec[0].r,{P}.rows.ec[0].q]")
    pg.click('button[data-tkt="r:wh"]'); pg.wait_for_timeout(150)
    res['r_type_all'] = pg.evaluate(f"{P}.rows.wh.every(r=>r.r==r.q)")
    res['ck_prog'] = pg.evaluate(f"tkProg({P},'r')")
    res['fp_same_after_r'] = pg.evaluate(f"fp({P})") == fp0
    pg.evaluate(f"V={{v:'sum',sm:'ck',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(250)
    open(OUT + 'checklist.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    res['ck_pdf_clone'] = pg.evaluate("(()=>{const c=pdfClone($('#rp'));return [c.querySelectorAll('button,input').length,c.querySelectorAll('tr.tot').length]})()")
    pg.reload(); pg.wait_for_timeout(2000)
    res['r_after_reload'] = pg.evaluate(f"[{P}.rows.fh[{i_fh}].r,{P}.rows.ec[0].r]")
    # print shortages from checklist
    pg.evaluate(f"V={{v:'sum',sm:'ck',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(200)
    pg.click('button[data-nq="r:ph"]'); pg.wait_for_timeout(250)
    res['nq_r_title'] = pg.inner_text('#rp .ph b')
    res['nq_r_total'] = pg.inner_text('#rp .ttot')
    pg.screenshot(path=OUT + '02_print_shortage.png', full_page=False)
    pg.click('button[data-nqb]'); pg.wait_for_timeout(200); res['back_from_nq'] = pg.evaluate("[V.v,V.sm]")
    # ---- execution tab ----
    pg.evaluate("V={v:'revhub',op:{},dr:{},q:V.q};render()"); pg.wait_for_timeout(150)
    pg.click('button[data-rh="exec"]'); pg.wait_for_timeout(200)
    res['exec_rows'] = pg.locator('button.xrow').count(); pg.screenshot(path=OUT + '03_exec_hub.png')
    pg.click(f'button.xrow[data-exg="{pid}"]'); pg.wait_for_timeout(250)
    res['exec_view'] = pg.evaluate("V.v")
    # Abdullah's example: required 2, executed 1 -> remaining 1
    i2 = pg.evaluate(f"{P}.rows.fh.findIndex(r=>+r.q==2)")
    pg.click(f'button[data-tk="x:fh:{i2}:1"]'); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT + '04_exec.png')
    res['x_set'] = pg.evaluate(f"[{P}.rows.fh[{i2}].q,{P}.rows.fh[{i2}].x,{P}.rows.fh[{i2}].r||0]")
    res['toast_warn'] = pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).join(' | ')")
    res['fp_same_after_x'] = pg.evaluate(f"fp({P})") == fp0
    res['rev_state'] = pg.evaluate(f"revSt({P})")
    pg.click('button[data-nq="x:ph"]'); pg.wait_for_timeout(250)
    nm2 = pg.evaluate(f"{P}.rows.fh[{i2}].nm")
    res['nq_x_example'] = pg.evaluate(f"[...document.querySelectorAll('#rp tr')].map(r=>r.innerText.replace(/\\s+/g,' ')).filter(t=>t.includes({json.dumps(nm2)}))")
    res['nq_x_total'] = pg.inner_text('#rp .ttot')
    res['nq_cols'] = pg.evaluate("[...document.querySelectorAll('#rp table')[0].rows[0].cells].map(c=>c.textContent)")
    # numbers consistent: remaining total == sum(q-x) in pieces
    res['nq_sum_check'] = pg.evaluate(f"(()=>{{const L=nqLines({P},'x');return [L.reduce((a,x)=>a+x.d,0),+document.querySelector('#rp .ttot b').textContent.replace(/\\D/g,'')]}})()")
    pg.screenshot(path=OUT + '05_exec_shortage.png', full_page=True)
    x = b64(pg, 'Promise.resolve(rpXlsx())'); open(OUT + 'nq_x_1533.xlsx', 'wb').write(x)
    z = zipfile.ZipFile(io.BytesIO(x)); res['nq_xlsx'] = re.findall(r'<sheet name="([^"]+)"', z.read('xl/workbook.xml').decode())
    open(OUT + 'nq_x_1533.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    res['fname'] = pg.evaluate('fname()')
    # month scope
    pg.click('button[data-nqs="mo"]'); pg.wait_for_timeout(300)
    res['nq_month'] = [pg.inner_text('#rp .ph b'), pg.locator('#rp h3.nqp').count(), pg.inner_text('#rp .ttot')]
    x = b64(pg, 'Promise.resolve(rpXlsx())'); open(OUT + 'nq_x_month.xlsx', 'wb').write(x)
    z = zipfile.ZipFile(io.BytesIO(x)); res['nq_month_xlsx'] = re.findall(r'<sheet name="([^"]+)"', z.read('xl/workbook.xml').decode()); res['nq_month_info'] = re.findall(r'<t xml:space="preserve">([^<]*)</t>', z.read('xl/worksheets/sheet2.xml').decode())
    pg.screenshot(path=OUT + '06_month_shortage.png')
    # all done case
    pg.evaluate(f"(()=>{{const p={P};ckRows(p).forEach(x=>x.r.x=qn(x.r));sv();V={{v:'nq',nk:'x',ns:'ph',p:p.id,mo:p.mo,from:'exec',op:{{}},dr:{{}},q:V.q}};render()}})()"); pg.wait_for_timeout(200)
    res['all_done'] = pg.inner_text('#rp .okall')
    res['rev_state_end'] = pg.evaluate(f"revSt({P})")
    # ---- swap Personal <-> Beauty (wh) ----
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{wh:true}},dr:{{}},fo:{{wh:1}},q:V.q}};render()"); pg.wait_for_timeout(200)
    pg.select_option('select[data-t="wh"][data-k="sec"]', 'Personal'); pg.wait_for_timeout(150)
    res['swap_btn'] = pg.inner_text('button[data-swp="wh"]')
    nm_p = pg.evaluate("V.dr.wh.nm")
    pg.click('button[data-swp="wh"]'); pg.wait_for_timeout(150)
    res['after_swap'] = pg.evaluate("[V.dr.wh.sec,V.dr.wh.nm]") + [nm_p]
    res['swap_btn2'] = pg.inner_text('button[data-swp="wh"]')
    pg.screenshot(path=OUT + '07_swap.png')
    n0 = pg.evaluate(f"{P}.rows.wh.length"); pg.click('button[data-add="wh"]'); pg.wait_for_timeout(200)
    res['swap_saved'] = pg.evaluate(f"(()=>{{const r={P}.rows.wh[{n0}];return [r.sec,r.nm,cl(r)]}})()")
    pg.select_option('select[data-t="wh"][data-k="sec"]', 'Health'); pg.wait_for_timeout(150)
    res['no_swap_health'] = pg.locator('button[data-swp]').count()
    # ---- picker ----
    pg.select_option('select[data-t="wh"][data-k="sec"]', 'Baby'); pg.wait_for_timeout(150)
    pg.click('button[data-nmp="wh"]'); pg.wait_for_timeout(500)
    res['picker'] = pg.evaluate("(()=>{const o=document.querySelector('.nmov');const c=[...o.querySelectorAll('.nmc')];const im=c.map(x=>x.querySelector('img')).filter(Boolean).filter(i=>i.complete&&i.naturalWidth);return {cards:c.length,opts:opts(T.find(t=>t.id=='wh').f.find(f=>f.k=='nm'),V.dr.wh,DB.ph.find(p=>p.id==V.p).sh).length,cols:Math.round(o.querySelector('.nmg').clientWidth/o.querySelector('.nmc').getBoundingClientRect().width),ratio:im.slice(0,4).map(i=>[Math.round(i.getBoundingClientRect().width),Math.round(i.getBoundingClientRect().height),+(i.naturalWidth/i.naturalHeight).toFixed(2),+(i.getBoundingClientRect().width/i.getBoundingClientRect().height).toFixed(2)]),label_px:getComputedStyle(c[0].querySelector('small')).fontSize}})()")
    pg.screenshot(path=OUT + '08_picker_wh.png')
    pg.fill('.nmq', 'milk'); pg.wait_for_timeout(150)
    res['search'] = pg.evaluate("[...document.querySelectorAll('.nmc')].filter(c=>!c.hidden).map(c=>c.dataset.nmv)")
    # long press -> zoom, no selection
    before = pg.evaluate("V.dr.wh.nm")
    box = pg.locator('.nmc:not([hidden])').first.bounding_box()
    pg.mouse.move(box['x'] + 20, box['y'] + 20); pg.mouse.down(); pg.wait_for_timeout(800); pg.mouse.up(); pg.wait_for_timeout(200)
    res['longpress'] = [pg.locator('.ovl.pov').count(), pg.evaluate("V.dr.wh.nm") == before]
    pg.click('.ovl.pov button[data-ovlx]'); pg.wait_for_timeout(100)
    pg.locator('.nmc:not([hidden])').first.click(); pg.wait_for_timeout(250)
    res['picked'] = pg.evaluate("[V.dr.wh.nm,!!document.querySelector('.nmov')]")
    # EG picker 2 columns + swap name
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{eg:true}},dr:{{}},fo:{{eg:1}},q:V.q}};render()"); pg.wait_for_timeout(200)
    pg.click('button[data-nmp="eg"]'); pg.wait_for_timeout(500)
    res['picker_eg'] = pg.evaluate("(()=>{const o=document.querySelector('.nmov');const i=[...o.querySelectorAll('.nmc img')].filter(i=>i.naturalWidth)[0];const r=i.getBoundingClientRect();return {cols:Math.round(o.querySelector('.nmg').clientWidth/o.querySelector('.nmc').getBoundingClientRect().width),w:Math.round(r.width),h:Math.round(r.height),nat:+(i.naturalWidth/i.naturalHeight).toFixed(2)}})()")
    pg.screenshot(path=OUT + '09_picker_eg.png')
    pg.evaluate("[...document.querySelectorAll('.nmc')].find(c=>/^Personal · /.test(c.dataset.nmv)).click()"); pg.wait_for_timeout(250)
    eg0 = pg.evaluate("V.dr.eg.nm"); pg.click('button[data-swp="eg"]'); pg.wait_for_timeout(150)
    res['eg_swap'] = pg.evaluate("[V.dr.eg.nm,!!imgOf(V.dr.eg.nm)]") + [eg0]
    pg.screenshot(path=OUT + '10_eg_swap.png')
    # ---- new type: Add to cart ----
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{ga:true}},dr:{{}},fo:{{ga:1}},q:V.q}};render()"); pg.wait_for_timeout(200)
    res['ga_in_types'] = pg.evaluate(f"TY({P}).some(t=>t.id=='ga')")
    pg.fill('input[data-t="ga"][data-k="q"]', '3'); pg.click('button[data-add="ga"]'); pg.wait_for_timeout(200)
    res['ga_row'] = pg.evaluate(f"{P}.rows.ga")
    pg.evaluate(f"V={{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(250)
    res['ga_sum'] = pg.evaluate("(()=>{const h=[...document.querySelectorAll('#rp h3')].find(h=>h.textContent=='ضفها للسلة');const t=h.nextElementSibling.querySelector('table');return [...t.rows].map(r=>r.innerText.replace(/\\s+/g,' '))})()")
    res['ga_tsum'] = pg.evaluate("[...document.querySelectorAll('#rp table.tsum tr')].map(r=>r.innerText.replace(/\\s+/g,' ')).filter(t=>/ضفها/.test(t))")
    res['ga_ttot'] = pg.evaluate("[...document.querySelectorAll('#rp .ttot')].map(x=>x.innerText.replace(/\\s+/g,' ')).filter(t=>/ضفها/.test(t))")
    y = pg.evaluate("(()=>{const h=[...document.querySelectorAll('#rp h3')].find(h=>h.textContent=='ضفها للسلة');return h.getBoundingClientRect().top+scrollY-120})()"); pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(150); pg.screenshot(path=OUT + '11_ga_summary.png')
    pg.click('button[data-sm="mgmt"]'); pg.wait_for_timeout(200)
    res['ga_mgmt'] = pg.evaluate("[...document.querySelectorAll('#rp tr')].map(r=>r.innerText.replace(/\\s+/g,' ')).filter(t=>/ضفها/.test(t))")
    # exec 1 of 3 -> shortages 4 side, 8 header
    gi = pg.evaluate(f"{P}.rows.ga.length-1")
    pg.evaluate(f"(()=>{{const p={P};p.rows.ga[{gi}].x=1;sv();V={{v:'nq',nk:'x',ns:'ph',p:p.id,mo:p.mo,from:'exec',op:{{}},dr:{{}},q:V.q}};render()}})()"); pg.wait_for_timeout(200)
    res['ga_short'] = pg.evaluate("[...document.querySelectorAll('#rp tr')].map(r=>r.innerText.replace(/\\s+/g,' ')).filter(t=>/سايد|هيدر/.test(t))")
    res['month_q'] = pg.evaluate(f"mStats([{P}]).q")
    # ---- English ----
    left = {}
    for name, js in [('ck', f"V={{v:'sum',sm:'ck',p:{pid},op:{{}},dr:{{}},q:V.q}}"), ('exec', f"V={{v:'exec',p:{pid},op:{{}},dr:{{}},q:V.q}}"), ('hub', "RHT='exec';V={v:'revhub',op:{},dr:{},q:V.q}"), ('nq', f"V={{v:'nq',nk:'x',ns:'ph',p:{pid},mo:'2026-10',from:'exec',op:{{}},dr:{{}},q:V.q}}"), ('form', f"V={{v:'ph',p:{pid},op:{{wh:true,ga:true}},dr:{{}},fo:{{wh:1,ga:1}},q:V.q}}")]:
        pg.evaluate(f"DB.cfg.lang='en';{js};render();cfg()"); pg.wait_for_timeout(250)
        t = pg.evaluate("document.body.innerText"); left[name] = sorted(set(x.strip() for x in AR.findall(t) if x.strip()))
        pg.screenshot(path=OUT + f'12_en_{name}.png', full_page=False)
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{wh:true}},dr:{{}},fo:{{wh:1}},q:V.q}};render()"); pg.wait_for_timeout(150); pg.click('button[data-nmp="wh"]'); pg.wait_for_timeout(300)
    t = pg.evaluate("document.querySelector('.nmov').innerText"); left['picker'] = sorted(set(x.strip() for x in AR.findall(t) if x.strip()))
    res['en_left'] = left
    pg.evaluate("document.querySelector('.nmov').remove();DB.cfg.lang='';cfg();render()")
    # full backup carries r/x
    with pg.expect_download() as dd:
        pg.evaluate("window.showSaveFilePicker=undefined;navigator.canShare=()=>false;V={v:'bk',op:{},dr:{},q:V.q};render()"); pg.click('button[data-bkp]')
    dd.value.save_as(OUT + 'bk.json'); j = json.load(open(OUT + 'bk.json', encoding='utf-8'))
    pj = [p for p in j['ph'] if p['no'] == '1533'][0]
    res['backup_rx'] = [sum(1 for r in pj['rows']['fh'] if 'x' in r), sum(1 for r in pj['rows']['fh'] if 'r' in r)]
    res['dialogs'] = dl[-8:]
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('\n'.join(errs) or 'NO ERRORS')

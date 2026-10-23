import json, os, base64, re
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'
S9 = W + 's9/'
d = json.load(open(W + 'out3/966-data-v1.3.json', encoding='utf-8'))
# add pharmacy 652 (new, no rows) for import test
d['ph'].append({'id': 99652, 'no': '652', 'rg': 'الشمالية', 'ct': 'تبوك', 'name': '', 'sh': 0, 'mo': '2026-10', 'st': 'لم تبدأ', 'sup': 'عبدالله السواح', 'co': 'عمال الشركة', 'mod': 'براندنج جديد', 'rows': {'ab': []}, 'm1': 1, 'm2': 1})
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
    dl = []
    pg.on('dialog', lambda x: (dl.append(x.message[:70]), x.accept()))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>{localStorage.setItem('ads',d)}", DATA); pg.reload(); pg.wait_for_timeout(1800)
    sh = lambda n, f=False: pg.screenshot(path=W + f's9/{n}.png', full_page=f)
    # 1. image library import
    pg.click('button.hmb'); pg.click('button[data-mgo="imgs"]'); pg.wait_for_timeout(200); sh('01_imgs_empty')
    pg.set_input_files('#imgx', S9 + 'Photo Wall & Floor Header & Header Gandola.xlsx'); pg.wait_for_timeout(4000)
    res['imr'] = pg.evaluate("V.v=='imr'?[V.imr.items.length,V.imr.items.filter(x=>x.nm).length,V.imr.items.filter(x=>x.chk).length]:V.v")
    res['imr_chk'] = pg.evaluate("V.imr.items.map((x,i)=>[i,x.raw,x.nm,x.chk]).filter(x=>x[3])")
    sh('02_imr', True)
    pg.click('button[data-imrgo]'); pg.wait_for_timeout(600)
    _c = -1
    for _ in range(40):  # wait until the image import has finished (count stable)
        n = pg.evaluate("Object.keys(IMG).length")
        if n == _c: break
        _c = n; pg.wait_for_timeout(700)
    res['img_count'] = pg.evaluate("Object.keys(IMG).length"); sh('03_imgs_after')
    # 1b import gandola images from pharmacy file
    pg.set_input_files('#imgx', S9 + 'New Headers-P0652.xlsx'); pg.wait_for_timeout(3500)
    res['imr652'] = pg.evaluate("[V.imr.items.length,V.imr.items.filter(x=>x.nm).length,V.imr.items.filter(x=>/·/.test(x.nm)).map(x=>x.nm)]")
    pg.click('button[data-imrgo]'); pg.wait_for_timeout(600)
    _c = -1
    for _ in range(40):  # wait until the second import has finished too
        n = pg.evaluate("Object.keys(IMG).length+'|'+V.v")
        if n == _c: break
        _c = n; pg.wait_for_timeout(700)
    res['img_count2'] = pg.evaluate("Object.keys(IMG).length")
    # 2. summary with images
    pid = pg.evaluate("DB.ph.find(p=>p.no=='1533').id")
    pg.evaluate(f"V={{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(300)
    res['sum_imgs'] = pg.locator('#rp td.nic img').count()
    y = pg.evaluate("(()=>{const h=[...document.querySelectorAll('#rp h3')].find(h=>/Wall Header/.test(h.textContent));return h.getBoundingClientRect().top+scrollY-120})()")
    pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(200); sh('04_sum')
    open(W + 's9/sum1533.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    # 3. pharmacy page rows + form
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{fh:true,__att:true}},dr:{{}},fo:{{fh:1}},q:V.q}};render()"); pg.wait_for_timeout(200)
    res['rw_imgs'] = pg.locator('.rwimg').count(); res['form_img'] = pg.locator('details[data-id="fh"] .fimg').count()
    # 4. attach Excel to 1533 -> compare
    pg.set_input_files('#attxls', S9 + 'New Headers-P1533.xlsx'); pg.wait_for_timeout(4000)
    res['xr1533_view'] = pg.evaluate("V.v")
    print(json.dumps(res,ensure_ascii=False)[:3000], dl, errs, flush=True)
    res['xr1533'] = pg.evaluate("(()=>{const X=V.xr;return{items:X.items.length,bad:X.items.filter(x=>x.inc&&x.bad).map(x=>x.desc+'/'+x.raw),ask:X.items.filter(x=>x.inc&&x.ask).length}})()")
    res['xr1533_status'] = pg.evaluate("[...document.querySelectorAll('.xst')].map(x=>x.textContent).slice(0,40)")
    sh('05_xr1533', True)
    n0 = pg.evaluate(f"(DB.ph.find(p=>p.id=={pid}).rows.fh||[]).length")
    first_add = pg.locator('button[data-xadd]:not([data-xadd="*"])').first
    if first_add.count():
        first_add.click(); pg.wait_for_timeout(300)
    res['added_one'] = pg.evaluate(f"(DB.ph.find(p=>p.id=={pid}).rows.fh||[]).length+(DB.ph.find(p=>p.id=={pid}).rows.wh||[]).length") - n0
    res['att1533'] = pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).att")
    # 5. new pharmacy 652 import
    pg.evaluate("V={v:'ph',p:99652,op:{__att:true},dr:{},q:V.q};render()"); pg.wait_for_timeout(150)
    pg.set_input_files('#attxls', S9 + 'New Headers-P0652.xlsx'); pg.wait_for_timeout(4000)
    res['xr652'] = pg.evaluate("V.xr.items.map(x=>[x.t,x.desc,x.nm,x.sec,x.len||x.sz||'',x.q,x.bad?'BAD':'',x.ask?'ASK':''].join(' | '))")
    sh('06_xr652', True)
    pg.click('button[data-xgo]'); pg.wait_for_timeout(400)
    res['rows652'] = pg.evaluate("(()=>{const p=DB.ph.find(x=>x.id==99652);const o={};['wh','fh','eg','md'].forEach(t=>o[t]=(p.rows[t]||[]).map(r=>[r.sec||'',r.nm,r.len||r.sz||'',r.q].join('/')));return o})()")
    res['xmap'] = pg.evaluate("DB.cfg.xmap")
    # 6. plan attach (pdf) + image
    pg.evaluate("V={v:'ph',p:99652,op:{__att:true},dr:{},q:V.q};render()"); pg.wait_for_timeout(150)
    pg.set_input_files('#attplan', S9 + 'PH-652 - REV 01-Model.pdf'); pg.wait_for_timeout(600)
    res['plan_meta'] = pg.evaluate("DB.ph.find(x=>x.id==99652).att.plan")
    with ctx.expect_page() as np:
        pg.click('button[data-attopen="plan"]')
    res['pdf_open'] = np.value.url[:20]; np.value.close()
    pg.set_input_files('#attplan', S9 + 'PH-652 plan.jpg'); pg.wait_for_timeout(800)
    sh('07_att')
    pg.click('button.pr[data-attopen="plan"]'); pg.wait_for_timeout(300); res['ovl'] = pg.locator('.ovl img').count(); sh('07b_ovl'); pg.click('button[data-ovlx]')
    # 7. bulk attach
    pg.click('button[data-tab="bk"]'); pg.wait_for_timeout(150)
    pg.set_input_files('#attmulti', [S9 + 'MC-0036 - PH - 1533 Dawadmi REV 01-Model.pdf', S9 + 'PH-652 - REV 01-Model.pdf', S9 + 'New Headers-P0652.xlsx', S9 + 'New Headers-P1533.xlsx'])
    pg.wait_for_timeout(300)
    res['atb'] = pg.evaluate("V.atb.items.map(x=>[x.f.name,x.no,x.kind,x.pid])"); sh('08_atb', True)
    pg.click('button[data-atbgo]'); pg.wait_for_timeout(800)
    res['att_after_bulk'] = pg.evaluate("DB.ph.filter(p=>p.att).map(p=>[p.no,Object.keys(p.att).join(','),(p.att.plan||{}).rev||''])")
    # 8. backup with files + restore in new context
    with pg.expect_download() as dd:
        pg.evaluate("window.showSaveFilePicker=undefined;navigator.canShare=()=>false"); pg.click('button[data-bkpf]')
    dd.value.save_as(W + 's9/bkf.json')
    j = json.load(open(W + 's9/bkf.json', encoding='utf-8'))
    res['bkf'] = [len(j.get('_imgs', {})), len(j.get('_files', {})), os.path.getsize(W + 's9/bkf.json') // 1024]
    # english
    pg.evaluate("DB.cfg.lang='en';V={v:'imgs',op:{},dr:{},q:V.q};render()"); pg.wait_for_timeout(200)
    t = pg.evaluate("(()=>{const c=document.body.cloneNode(true);c.querySelectorAll('.toast').forEach(x=>x.remove());document.body.appendChild(c);c.style.cssText='position:absolute;left:0;top:0';const t=c.innerText;c.remove();return t})()"); res['en_imgs_left'] = sorted(set(x.strip() for x in AR.findall(t)))[:20]
    pg.evaluate("V={v:'ph',p:99652,op:{__att:true},dr:{},q:V.q};render()"); pg.wait_for_timeout(200)
    t = pg.evaluate("(()=>{const c=document.body.cloneNode(true);c.querySelectorAll('.toast').forEach(x=>x.remove());document.body.appendChild(c);c.style.cssText='position:absolute;left:0;top:0';const t=c.innerText;c.remove();return t})()"); res['en_ph_left'] = sorted(set(x.strip() for x in AR.findall(t)))[:20]
    pg.evaluate("DB.cfg.lang='';render()")
    ctx2 = br.new_context(viewport={'width': 400, 'height': 860}, accept_downloads=True)
    p2 = ctx2.new_page(); p2.on('pageerror', lambda e: errs.append('P2 ' + str(e))); p2.on('dialog', lambda x: x.accept())
    p2.goto(URL); p2.wait_for_timeout(1500); p2.click('button[data-tab="bk"]'); p2.wait_for_timeout(200)
    p2.set_input_files('#rst', W + 's9/bkf.json'); p2.wait_for_timeout(2500)
    res['restored'] = p2.evaluate("[DB.ph.length,Object.keys(IMG).length,!!(DB._imgs||DB._files)]")
    res['restored_blob'] = p2.evaluate("idbGet('f:99652:plan').then(b=>b?b.size:0)")
    res['ls_size_kb'] = p2.evaluate("Math.round((localStorage.getItem('ads')||'').length/1024)")
    res['dialogs'] = dl
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('\n'.join(errs) or 'NO ERRORS')

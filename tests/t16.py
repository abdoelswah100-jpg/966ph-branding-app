import json, os, re, base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';OUT=W+'s16/';os.makedirs(OUT,exist_ok=True)
DATA=open(W+'out6/966-data-v1.2.json',encoding='utf-8').read();JS=W+'mnt/صيانات 2026 الربع 3 و4 - للاستيراد.json';SY=open(W+'nov/966-sync - صيدليات شهر 11-2026.json',encoding='utf-8').read()
errs,res,dl=[],{},[]
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');ctx=br.new_context(viewport={'width':400,'height':860},device_scale_factor=2,accept_downloads=True);pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)));pg.on('console',lambda m:errs.append('CONSOLE '+m.text) if m.type=='error' else None);pg.on('dialog',lambda x:(dl.append(x.message[:140]),x.accept()))
    pg.goto('file://'+W+'new14.html');pg.wait_for_timeout(300);pg.evaluate("d=>{const o=JSON.parse(d);o.ph.push({id:5,no:'999',rg:'الشرقية',ct:'x',sh:-1,mo:'2026-11',rows:{}});localStorage.setItem('ads',JSON.stringify(o))}",DATA);pg.reload();pg.wait_for_timeout(1800)
    res['sh_fix']=pg.evaluate("DB.ph.find(p=>p.no=='999').sh")
    pg.evaluate("goV({v:'ph',p:5,op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);res['ph999_ok']=pg.evaluate("V.v")
    pg.click('button.hmb');pg.wait_for_timeout(150);pg.click('[data-mgo=mnt]');pg.wait_for_timeout(300);res['view']=pg.evaluate('V.v');pg.screenshot(path=OUT+'01_empty.png')
    pg.set_input_files('#mjson',JS);pg.wait_for_timeout(600);res['import']=dl[-1];res['cur']=pg.evaluate("[MU().cur,MU().items.length,mList(MU().cur).length]")
    pg.set_input_files('#mjson',JS);pg.wait_for_timeout(500);res['reimport']=dl[-1]
    pg.select_option('#mqsel','2026-Q3');pg.wait_for_timeout(300);res['q3']=pg.evaluate("[mList('2026-Q3').length,mList('2026-Q3').reduce((a,x)=>a+x.q,0),[...document.querySelectorAll('.mtab tr.mmo td')].map(t=>t.textContent)]")
    pg.screenshot(path=OUT+'02_q3.png',full_page=True)
    pg.select_option('#mqsel','2026-Q4');pg.wait_for_timeout(300)
    # add a job for pharmacy 1533 Floor Header -> size from shelf type
    pg.click('button[data-madd]');pg.wait_for_timeout(300)
    pg.fill('input[data-mf=ph]','1533');pg.dispatch_event('input[data-mf=ph]','change');pg.wait_for_timeout(200)
    pg.click('button[data-mwork="تغيير"]');pg.wait_for_timeout(150)
    pg.select_option('select[data-mf=ad]','Floor Header');pg.wait_for_timeout(200)
    pg.fill('input[data-mf=det]','فلور هيدر قسم العناية');pg.fill('input[data-mf=q]','2');pg.dispatch_event('input[data-mf=q]','change');pg.wait_for_timeout(200)
    res['draft']=pg.evaluate("[V.me.ct,V.me.sz,V.me.work,mStmt(V.me)]");pg.screenshot(path=OUT+'03_editor.png',full_page=True)
    pg.click('button[data-msave]');pg.wait_for_timeout(300)
    pg.click('button[data-mrep]');pg.wait_for_timeout(300);res['repeat']=pg.evaluate("[V.v,V.me.ph,V.me.ad,V.me.id!=MU().items.slice(-1)[0].id]");pg.click('button[data-msave]');pg.wait_for_timeout(300)
    pg.click('.mtab tr[data-med] >> nth=0');pg.wait_for_timeout(300);res['edit']=pg.evaluate("[V.v,V.me.ph]");pg.fill('input[data-mf=q]','5');pg.dispatch_event('input[data-mf=q]','change');pg.click('button[data-msave]');pg.wait_for_timeout(300)
    res['q4']=pg.evaluate("[mList('2026-Q4').length,mList('2026-Q4').reduce((a,x)=>a+x.q,0)]")
    pg.reload();pg.wait_for_timeout(1500);res['persist']=pg.evaluate("[MU().cur,MU().items.length]")
    pg.evaluate("goV({v:'mnt',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.evaluate('window.showSaveFilePicker=undefined')
    with pg.expect_download() as d: pg.click('button[data-mxl=save]')
    d.value.save_as(OUT+'mnt.xlsx');res['xname']=d.value.suggested_filename
    b=pg.evaluate("async()=>{const b=await buildPdf(mntPdfEl(MU().cur),'x');const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)}");open(OUT+'mnt.pdf','wb').write(base64.b64decode(b))
    pg.evaluate("DB.cfg.lang='en';svq();render()");pg.wait_for_timeout(400);t=pg.evaluate("document.querySelector('main').innerText");res['en_left']=sorted(set(re.findall(r'[ء-ي][ء-ي ]{2,}',t)))[:20];pg.screenshot(path=OUT+'04_en.png')
    br.close()
for k,v in res.items():print(k,'=>',v)
print('ERRS',errs[:8])

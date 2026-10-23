import json, os, base64, re
from playwright.sync_api import sync_playwright
W='/home/claude/work/'; OUT=W+'s14/'; os.makedirs(OUT,exist_ok=True)
d=json.load(open(W+'out6/966-data-v1.2.json',encoding='utf-8'))
d['cfg'].pop('lx',None)
DATA=json.dumps(d,ensure_ascii=False)
URL='file://'+W+'full28.html'
errs,res=[],{}
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx=br.new_context(viewport={'width':400,'height':860},device_scale_factor=2,accept_downloads=True)
    pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)))
    pg.on('console',lambda m:errs.append('CONSOLE '+m.text) if m.type=='error' else None)
    dl=[];pg.on('dialog',lambda x:(dl.append(x.message[:160]),x.accept()))
    pg.goto(URL);pg.wait_for_timeout(300)
    pg.evaluate("d=>localStorage.setItem('ads',d)",DATA);pg.reload();pg.wait_for_timeout(2200)
    res['ver']=pg.evaluate('VER'); res['title']=pg.title()
    res['nm_counts']=pg.evaluate("Object.fromEntries(Object.entries(NM).map(([k,v])=>[k,v.length]))")
    res['new_have']=pg.evaluate("['Anti-Lice','Korean Brands','Manuka Honey','Kids Toothpaste','Perfumes'].map(n=>[n,Object.keys(NM).filter(k=>NM[k].includes(n))])")
    res['img_perf']=pg.evaluate("[!!imgOf('Perfumes','Beauty'),!!imgOf('Perfumes','Personal'),imgOf('Perfumes','Beauty')!=imgOf('Perfumes','Personal')]")
    res['img_new_missing']=pg.evaluate("libNames().filter(x=>!imgOf(x.n,x.g)).map(x=>x.g+':'+x.n)")
    res['img_size']=pg.evaluate("new Promise(ok=>{const i=new Image();i.onload=()=>ok([i.naturalWidth,i.naturalHeight]);i.src=imgOf('Anti-Lice','Baby')})")
    res['imgsz']=pg.evaluate("[IMGSZ('Anti-Lice'),IMGSZ('Personal · Deo')]")
    res['col']=pg.evaluate("[COL.Baby,COL.Beauty,COL.Health,COL.Personal,COL.Medicated]")
    res['fh_secs']=pg.evaluate("T.find(t=>t.id=='fh').f[0].o()")
    res['fh_med_opts']=pg.evaluate("(()=>{const f=T.find(t=>t.id=='fh').f[1];return f.o({sec:'Medicated'}).length+'/'+MED.length})()")
    pid=pg.evaluate("DB.ph.find(p=>p.rows&&p.rows.fh&&p.rows.fh.length).id"); P=f"DB.ph.find(p=>p.id=={pid})"
    # add Medicated floor header via the form
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{fh:true}},dr:{{}},q:V.q,fo:{{fh:1}}}};render()");pg.wait_for_timeout(300)
    pg.select_option('select[data-t="fh"][data-k="sec"]','Medicated');pg.wait_for_timeout(250)
    n0=pg.evaluate(f"{P}.rows.fh.length")
    pg.evaluate("V.dr.fh.nm=MED[0]");pg.evaluate("render()");pg.wait_for_timeout(150)
    pg.screenshot(path=OUT+'01_fh_med_form.png')
    pg.click('button[data-add="fh"]');pg.wait_for_timeout(300)
    res['fh_added']=pg.evaluate(f"(()=>{{const a={P}.rows.fh;return [a.length-{n0},a[a.length-1].sec,a[a.length-1].nm,T.find(t=>t.id=='fh').z(a[a.length-1],{P}.sh)]}})()")
    # notes input keyboard
    res['inputmodes']=pg.evaluate("(()=>{V={v:'ph',p:"+str(pid)+",op:{wh:true},dr:{},q:V.q,fo:{wh:1}};render();return [...document.querySelectorAll('input[data-t]')].map(i=>i.dataset.k+':'+i.type+':'+(i.getAttribute('inputmode')||'-'))})()")
    # summary with medicated colour
    pg.evaluate(f"V={{v:'sum',sm:'sum',p:{pid},op:{{}},dr:{{}},q:V.q}};render()");pg.wait_for_timeout(300)
    res['sum_has_med']='Medicated' in pg.inner_text('#rp')
    pg.screenshot(path=OUT+'02_summary.png',full_page=True)
    # checklist title + tracking width
    pg.evaluate(f"V={{v:'sum',sm:'ck',p:{pid},op:{{}},dr:{{}},q:V.q}};render()");pg.wait_for_timeout(300)
    res['ck_title_html']=pg.evaluate("document.querySelector('#rp .ph b').innerHTML.slice(0,90)")
    res['ck_overflow']=pg.evaluate("[document.documentElement.scrollWidth,innerWidth,Math.max(...[...document.querySelectorAll('.tkt')].map(t=>t.getBoundingClientRect().right))]")
    pg.screenshot(path=OUT+'03_checklist.png')
    pg.click('button.tkb[data-tk], button[data-tk]');pg.wait_for_timeout(150)
    # set some r/x, check card
    pg.evaluate(f"(()=>{{const p={P};p.rows.fh.forEach(r=>{{r.r=r.q}});p.rows.fh[0].x=p.rows.fh[0].q;sv()}})()")
    pg.evaluate("V={v:'home',op:{},dr:{},q:{t:'',st:'',mo:''}};render()");pg.wait_for_timeout(300)
    res['card_tk']=pg.evaluate("[...document.querySelectorAll('.pc-tk')].map(x=>x.textContent).slice(0,3)")
    res['sync_banner']=pg.evaluate("syncBanner().replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').slice(0,220)")
    pg.screenshot(path=OUT+'04_home.png')
    # shortages text + buttons
    pg.evaluate(f"V={{v:'nq',p:{pid},nk:'x',ns:'ph',mo:{P}.mo,op:{{}},dr:{{}},q:V.q}};render()");pg.wait_for_timeout(300)
    res['nq_btns']=pg.evaluate("[!!document.querySelector('[data-nqtxt]'),!!document.querySelector('[data-nqpdf]'),V.v]")
    res['nq_text']=pg.evaluate("nqText()")
    pg.screenshot(path=OUT+'05_nq.png')
    pg.evaluate("window.open=u=>{window._wa=u}");pg.evaluate("delete navigator.share");pg.click('[data-nqtxt]');pg.wait_for_timeout(300)
    res['wa']=pg.evaluate("(window._wa||'').slice(0,60)")
    # sync: version stamp + older file warning
    res['sync_ver']=pg.evaluate("(()=>{try{return JSON.stringify(syncPayload?syncPayload():{}).includes('\"ver\":\"v1.3\"')}catch(e){return 'nofn'}})()")
    res['verN']=pg.evaluate("[verN('v1.2')<verN('v1.3'),verN('v1.10')>verN('v1.3'),verN(undefined)<verN('v1.3')]")
    # sounds
    res['snd']=pg.evaluate("(()=>{['tick','ok','warn','err'].forEach(snd);toastT('⚠ تجربة');return typeof ACX})()")
    pg.evaluate("V={v:'gen',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(300)
    res['snd_toggle']=pg.evaluate("[!!document.getElementById('cfsnd'),!!document.getElementById('cfvib')]")
    pg.click('#cfsnd');pg.wait_for_timeout(100);res['snd_off']=pg.evaluate("DB.cfg.snd")
    pg.screenshot(path=OUT+'06_settings.png')
    # backup tab: laptop folder
    pg.evaluate("V={v:'bk',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(300)
    res['bkdir']=pg.evaluate("[FSA(),!!document.querySelector('[data-bkdir]')]")
    pg.screenshot(path=OUT+'07_backup.png',full_page=True)
    # English
    pg.evaluate("DB.cfg.lang='en';sv();V={v:'gen',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(500)
    res['en_gen']=pg.evaluate("document.body.innerText.includes('Sound and vibration')")
    pg.evaluate("V={v:'bk',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('.toast').forEach(x=>x.remove())");t=pg.evaluate("document.body.innerText");res['en_bk_ar']=re.findall(r'[ء-ي][ء-ي ]{3,}',t)[:8]
    br.close()
for k,v in res.items(): print(k,'=>',v)
print('dialogs',dl);print('ERRS',errs[:10])

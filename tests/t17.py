import json, os
from playwright.sync_api import sync_playwright
W='/home/claude/work/';OUT=W+'s17/';os.makedirs(OUT,exist_ok=True)
DATA=open(W+'out6/966-data-v1.2.json',encoding='utf-8').read();errs,res,dl=[],{},[]
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860},device_scale_factor=2)
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('dialog',lambda x:(dl.append(x.message[:100]),x.accept()))
    pg.goto('file://'+W+'new.html');pg.wait_for_timeout(300);pg.evaluate("d=>localStorage.setItem('ads',d)",DATA);pg.reload();pg.wait_for_timeout(1500)
    pid=pg.evaluate("DB.ph.find(p=>p.no=='1533').id");P=f"DB.ph.find(p=>p.id=={pid})"
    res['shelf']=pg.evaluate(f"SH[{P}.sh]")
    pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{fh:true}},dr:{{}},q:V.q,fo:{{fh:1}}}})");pg.wait_for_timeout(300)
    pg.select_option('select[data-t="fh"][data-k="sec"]','Health');pg.wait_for_timeout(200)
    res['rsh_opts']=pg.evaluate("[...document.querySelector('select[data-t=fh][data-k=rsh]').options].map(o=>o.text)")
    pg.select_option('select[data-t="fh"][data-k="rsh"]','New Turkish');pg.wait_for_timeout(200)
    pg.evaluate("V.dr.fh.nm='Vitamins'||V.dr.fh.nm;render()");pg.wait_for_timeout(150)
    pg.screenshot(path=OUT+'01_form.png',full_page=False)
    n0=pg.evaluate(f"{P}.rows.fh.length");pg.click('button[data-add="fh"]');pg.wait_for_timeout(300)
    res['added']=pg.evaluate(f"(()=>{{const p={P},r=p.rows.fh[p.rows.fh.length-1],t=T.find(t=>t.id=='fh');return [p.rows.fh.length-{n0},r.rsh,t.z(r,p.sh),t.z(Object.assign({{}},r,{{rsh:''}}),p.sh)]}})()")
    res['card_tag']=pg.evaluate("[...document.querySelectorAll('.rw .rshc')].map(x=>x.textContent)")
    pg.screenshot(path=OUT+'02_card.png')
    # medicated + end gandola on other shelves
    pg.evaluate(f"(()=>{{const p={P};p.rows.md=(p.rows.md||[]).concat([{{nm:'AVENE',q:1,rsh:'Old Turkish'}}]);p.rows.eg=(p.rows.eg||[]).concat([{{nm:'Personal · Deodorant',sz:'صغير',q:1,rsh:'Old Turkish'}}]);sv()}})()")
    res['md_z']=pg.evaluate(f"(()=>{{const p={P};const t=T.find(t=>t.id=='md');return [t.z(p.rows.md.slice(-1)[0],p.sh)]}})()")
    res['eg_z']=pg.evaluate(f"(()=>{{const p={P};const t=T.find(t=>t.id=='eg');return t.z(p.rows.eg.slice(-1)[0],p.sh)}})()")
    res['sizes']=pg.evaluate(f"sizeRows([{P}]).filter(x=>/Floor Header|Medicated|End gandola/.test(x.n)).map(x=>x.n+' '+x.sz+' '+x.mat+' ×'+x.q)")
    res['mgmt_eg']=pg.evaluate(f"managementReportRows([{P}]).filter(x=>x.kind=='eg').map(x=>[x.sz,x.shelf,x.pocket,x.header,x.side])")
    for sm in ('print','ck','mgmt'):
        pg.evaluate(f"goV({{v:'sum',sm:'{sm}',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
        res['tags_'+sm]=pg.evaluate("[...document.querySelectorAll('#rp .rshc')].map(x=>x.textContent)")
        pg.screenshot(path=OUT+f'03_{sm}.png',full_page=True)
    pg.evaluate(f"goV({{v:'nq',nk:'r',ns:'ph',p:{pid},mo:{P}.mo,op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);res['tags_nq']=pg.evaluate("[...document.querySelectorAll('#rp .rshc')].map(x=>x.textContent)")
    # duplicate warning still works for an old item re-added with 'same as pharmacy'
    r0=pg.evaluate(f"(()=>{{const r={P}.rows.fh[0];return {{sec:r.sec,nm:r.nm,sz:r.sz}}}})()")
    pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{fh:true}},dr:{{fh:Object.assign({{}},{json.dumps(r0)},{{q:1}})}},q:V.q,fo:{{fh:1}}}})");pg.wait_for_timeout(200)
    pg.click('button[data-add="fh"]');pg.wait_for_timeout(300);res['dup']=[x for x in dl if 'نفس' in x][:1]
    pg.evaluate("DB.cfg.lang='en';svq();goV({v:'sum',sm:'print',p:%d,op:{},dr:{},q:V.q})"%pid);pg.wait_for_timeout(400);res['en_tag']=pg.evaluate("[...document.querySelectorAll('#rp .rshc')].map(x=>x.textContent)")
    br.close()
for k,v in res.items():print(k,'=>',v)
print('ERRS',errs)

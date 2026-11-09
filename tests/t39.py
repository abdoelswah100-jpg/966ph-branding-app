# v3.4 part 2: custody handover, maintenance tab, home = branding only, folded types, old stock, out-of-stock alert
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new34.html';D=open(W+'bk1106/data.json',encoding='utf-8').read()
CJ=W+'cust/عهدة شهر 10-2026 - للاستيراد.json'
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860},accept_downloads=True);E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];FL=[];ANS=[]
  def dlg(x):
    DL.append(x.message[:220])
    if x.type=='prompt':x.accept(ANS.pop(0) if ANS else '')
    else:x.accept()
  pg.on('dialog',dlg);pg.on('download',lambda d:FL.append(d.suggested_filename))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  # ---- home / tabs / menu
  out('tabs',pg.evaluate("[...document.querySelectorAll('.bnav button')].map(b=>b.dataset.tab)"))
  out('home',pg.evaluate("[document.querySelector('#hcnt').innerText,[...document.querySelectorAll('#hl .pcard')].length,DB.ph.filter(isBr).length,DB.ph.filter(isMnt).length,!!document.querySelector('.schip'),!!document.querySelector('.schip[open]')]"))
  pg.click('.hmb');pg.wait_for_timeout(200);out('menu',pg.evaluate("[...document.querySelectorAll('.hmenu [data-mgo]')].map(b=>b.dataset.mgo).slice(0,4)"));pg.click('.hmenu [data-mgo=bk]');pg.wait_for_timeout(300)
  out('bk_view',pg.evaluate("[V.v,document.querySelector('header').innerText.replace(/\\s+/g,' ')]"))
  # ---- maintenance tab
  pg.click('.bnav [data-tab=mnt]');pg.wait_for_timeout(300)
  out('mnt',pg.evaluate("[V.v,[...document.querySelectorAll('main details.lst')].map(d=>[d.dataset.id,d.open]),document.querySelector('.bnav .on').dataset.tab]"))
  pg.click('details[data-id=__mph]>summary');pg.wait_for_timeout(200)
  out('mnt_groups',pg.evaluate("[...document.querySelectorAll('details[data-id=__mph] details.mg')].map(d=>[d.dataset.id,d.open,d.querySelectorAll('.pcard').length])"))
  pg.fill('#mpq','1');pg.dispatch_event('#mpq','change');pg.wait_for_timeout(300);out('mnt_search',pg.evaluate("document.querySelectorAll('details[data-id=__mph] .pcard').length"))
  pg.evaluate("V.mpq='';render()");pg.click('[data-newpm]');pg.wait_for_timeout(300);out('newpm',pg.evaluate("[V.v,$('#pmod').value]"))
  # ---- pharmacy screen: folded types / tools
  pid=pg.evaluate("DB.ph.find(p=>String(p.no)=='510').id")
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('ph_fold',pg.evaluate("[document.querySelector('.pemp summary').innerText.split('\\n')[0],!!document.querySelector('.pemp [data-fo]'),!!document.querySelector('.ptl [data-save]')]"))
  pg.click('.pemp>summary');pg.wait_for_timeout(150);t0=pg.evaluate("document.querySelector('.pemp details').dataset.id")
  out('fold_open_type',t0)
  # ---- old stock add + offer
  pg.evaluate("goV({v:'who',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
  pg.select_option('select[data-wo=k]','bfh');pg.wait_for_timeout(150);pg.select_option('select[data-wo=sh]','1');pg.wait_for_timeout(150)
  out('who_sizes',pg.evaluate("[...document.querySelectorAll('select[data-wo=sz] option')].map(o=>o.value)"))
  pg.fill('[data-wo=q]','4');pg.dispatch_event('[data-wo=q]','change');pg.click('[data-whosave]');pg.wait_for_timeout(300)
  pg.select_option('select[data-wo=k]','egs');pg.wait_for_timeout(150);pg.fill('[data-wo=q]','6');pg.dispatch_event('[data-wo=q]','change');pg.click('[data-whosave]');pg.wait_for_timeout(300)
  out('old_items',pg.evaluate("WU().filter(x=>x.old).map(x=>[x.ty,x.sh,x.nm,x.size,x.qty,x.mat])"))
  out('fh_offer',pg.evaluate(f"(p=>{{const t=T.find(x=>x.id=='fh');const i=p.rows.fh.findIndex(r=>whOldOpts(p,t,r).length);return i<0?null:[i,whOldOpts(p,t,p.rows.fh[i]).map(o=>o.txt)]}})(DB.ph.find(p=>p.id=={pid}))"))
  out('eg_offer',pg.evaluate(f"(p=>{{const t=T.find(x=>x.id=='eg');return (p.rows.eg||[]).map(r=>[r.nm,whOldOpts(p,t,r).map(o=>o.txt)])}})(DB.ph.find(p=>p.id=={pid}))"))
  # take one from the toast
  r=pg.evaluate(f"(p=>{{const t=T.find(x=>x.id=='fh');return p.rows.fh.findIndex(r=>whOldOpts(p,t,r).length)}})(DB.ph.find(p=>p.id=={pid}))")
  if r is not None and r>=0:
    pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{fh:1}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.click(f'[data-whfrom="fh:{r}"]');pg.wait_for_timeout(200)
    j=pg.evaluate("[...document.querySelectorAll('.toast [data-whf2]')].findIndex(b=>b.innerText.includes('🕰'))");pg.click(f'.toast [data-whf2="{j}"]');pg.wait_for_timeout(300)
    out('old_taken',pg.evaluate(f"[WU().find(x=>x.ty==OLDT.bfh).qty,DB.ph.find(p=>p.id=={pid}).rows.fh[{r}].wo,DB.wlog[0].note]"))
  pg.evaluate("goV({v:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.click('[data-whold]');pg.wait_for_timeout(200)
  out('wh_old_chip',pg.evaluate("[...document.querySelectorAll('.whc .whi b')].map(b=>b.textContent).slice(0,4)"))
  # out-of-stock alert
  pg.evaluate(f"""(()=>{{const p=DB.ph.find(x=>x.id=={pid}),t=T.find(x=>x.id=='fh'),r=p.rows.fh.find(r=>qn(r)-(+r.r||0)>0);const y=whParts(t,r,p.sh)[0];const x=whAdd({{sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:y.mat,size:y.size}},2,'in','manual','t');whAdd(x,-2,'out','manual','t');sv();V.wf={{}};goV({{v:'wh',op:{{}},dr:{{}},q:V.q}})}})()""");pg.wait_for_timeout(300)
  out('out_dbg',pg.evaluate("whOut().length"));out('out_alert',pg.evaluate("(e=>e&&e.innerText.replace(/\\s+/g,' ').slice(0,200))(document.querySelector('.wout'))"))
  # ---- custody handover
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#cjson',CJ);pg.wait_for_timeout(800)
  k0=pg.evaluate("CU().cur");rem0=pg.evaluate("cRem(cMo())")
  pg.click('[data-cdl]');pg.wait_for_timeout(200)
  out('dl_sheet',pg.evaluate("[document.querySelector('.csh b').innerText,[...document.querySelectorAll('.csh input[name=cdlo]')].map(i=>[i.value,i.checked])]"))
  FL.clear();pg.click('[data-cdgo=save]');pg.wait_for_timeout(6000)
  out('dl_files',FL)
  out('dl_state',pg.evaluate(f"(C=>[C.cur,C.m['{k0}'].dl&&[C.m['{k0}'].dl.rem,C.m['{k0}'].dl.nx,C.m['{k0}'].dl.ov],C.m[C.cur].open,C.m[C.cur].why])(CU())"))
  # old month is locked
  pg.evaluate(f"CU().cur='{k0}';render()");pg.wait_for_timeout(200)
  out('locked',pg.evaluate("[document.querySelector('.cdlv').innerText.replace(/\\s+/g,' '),!!document.querySelector('.cbtn[hidden]'),!document.querySelector('[data-cdl]')]"))
  n0=len(DL);pg.evaluate("document.querySelector('tr[data-ced]').click()");pg.wait_for_timeout(200);out('lock_toast',[pg.evaluate("V.v"),pg.evaluate("(t=>t&&t.innerText)([...document.querySelectorAll('.toast')].pop())")])
  # reopen, change an amount, hand over again -> asks to update next month opening
  pg.click('[data-cdreo]');pg.wait_for_timeout(200);out('reopened',pg.evaluate("[cMo().reo,document.querySelector('[data-cdl]').innerText]"))
  pg.evaluate("(()=>{const x=cMo().items.find(x=>!x.qt);x.amt=+x.amt+50;sv();render()})()");pg.wait_for_timeout(200)
  out('changed_note',pg.evaluate("document.querySelector('.cdlv').innerText.includes('اتعدّلت')"))
  n0=len(DL);FL.clear();pg.click('[data-cdl]');pg.wait_for_timeout(200);pg.click('[data-cdgo=save]');pg.wait_for_timeout(6000)
  out('redeliver',[DL[n0:],FL,pg.evaluate(f"(C=>[C.m['{k0}'].reo,C.m['{k0}'].dl.rem,C.m[C.m['{k0}'].dl.nx].open])(CU())")])
  out('ERRS',E);br.close()

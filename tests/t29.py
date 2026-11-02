# v2.5: photo limits, second layout, share before/after with text
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new25.html';D=open(W+'bk1102/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');ctx=br.new_context(viewport={'width':400,'height':860});pg=ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)));DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:80]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2000)
  out('defaults',pg.evaluate("[phMax('b'),phMax('a'),phMax('o')]"))
  pid=pg.evaluate("DB.ph.find(p=>p.no=='843').id")
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{__pho:true,__att:true}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('counters',pg.evaluate("[...document.querySelectorAll('.phh small')].map(s=>s.innerText)"))
  # add 3 after photos then share
  pg.evaluate("()=>{}")
  for i in range(3):
    pg.evaluate(f"(async()=>{{const r=await fetch('file:///home/claude/work/tim{i}.jpg').catch(()=>null);}})()")
  fs=[W+f'tim{i}.jpg' for i in range(3)]
  pg.evaluate("()=>{const i=document.createElement('input');i.type='file';i.id='tfa';i.multiple=true;document.body.appendChild(i)}")
  pg.set_input_files('#tfa',fs)
  pg.evaluate("(async()=>{const p=curP();await phoAdd(p,'a',[...document.querySelector('#tfa').files]);await phoAdd(p,'b',[document.querySelector('#tfa').files[0]]);render()})()");pg.wait_for_timeout(2500)
  out('photos',pg.evaluate("[phoList(curP(),'b').length,phoList(curP(),'a').length,[...document.querySelectorAll('[data-phshare]')].map(b=>b.dataset.phshare)]"))
  pg.evaluate("()=>{window._sh=null;navigator.canShare=()=>true;navigator.share=async o=>{window._sh={n:o.files.map(f=>f.name),t:o.text}}}")
  pg.click("[data-phshare=a]");pg.wait_for_timeout(1200);out('share_a',pg.evaluate("window._sh"))
  pg.click("[data-phshare=ba]");pg.wait_for_timeout(1200);out('share_ba',pg.evaluate("window._sh"))
  # settings
  pg.evaluate("goV({v:'gen',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  pg.fill('#cfpha','3');pg.dispatch_event('#cfpha','change');pg.wait_for_timeout(200)
  out('set',pg.evaluate("[DB.cfg.phA,phMax('a')]"))
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{__pho:true,__att:true}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('full_a',pg.evaluate("[...document.querySelectorAll('.phb')].map(b=>b.innerText.replace(/\\s+/g,' ').slice(0,70))"))
  # layouts
  out('att0',pg.evaluate("[...document.querySelectorAll('#app [data-attpick]')].map(b=>b.dataset.attpick)"))
  pg.set_input_files('#attplan',W+'tim0.jpg');pg.wait_for_timeout(1200)
  out('att1',pg.evaluate("[Object.keys(curP().att||{}),[...document.querySelectorAll('#app [data-attpick]')].map(b=>b.dataset.attpick)]"))
  pg.set_input_files('#attplan2',W+'tplan.pdf');pg.wait_for_timeout(1200)
  out('att2',pg.evaluate("[Object.entries(curP().att).map(([k,v])=>[k,v.n,!!v.th]),document.querySelector('details[data-id=__att] summary').innerText]"))
  out('slot',pg.evaluate("[planSlot(curP(),{name:'x.pdf',type:'application/pdf'}),planSlot(curP(),{name:'x.jpg',type:'image/jpeg'}),planSlot({att:{}},{name:'a.pdf'})]"))
  pg.click("[data-attdel=plan2]");pg.wait_for_timeout(300);out('del2',pg.evaluate("Object.keys(curP().att)"))
  out('dialogs',DL);out('ERRS',E)
  br.close()

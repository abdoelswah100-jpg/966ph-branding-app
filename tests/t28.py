# v2.4: locParse formats, route table, location update (mocked native http), buttons
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new24.html';D=open(W+'bk1102/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  ctx=br.new_context(viewport={'width':400,'height':860},geolocation={'latitude':24.7136,'longitude':46.6753},permissions=['geolocation'])
  pg=ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2000)
  out('parse',pg.evaluate("""[locParse('https://www.google.com/maps/place/Al+Dawaa/@24.6100,46.7200,17z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!8m2!3d24.6123!4d46.7234'),
    locParse('https://www.google.com/maps/search/24.501030,+44.374954?entry=tts'),locParse('https://maps.google.com/?q=24.71,46.67&ftid=1'),
    locParse('x window.APP_INITIALIZATION_STATE=[[[3352.1,46.6611,24.7222],[0,0,0]'),locParse('nothing here')]"""))
  out('needLoc',pg.evaluate("DB.ph.filter(needLoc).map(p=>p.no)"))
  # mock native http and update all
  pg.evaluate("""()=>{let i=0;window.Capacitor={isNativePlatform:()=>true,Plugins:{CapacitorHttp:{request:async({url})=>{i++;return {url:'https://www.google.com/maps/place/x/@24.'+(600+i)+',46.'+(700+i)+',17z/data=!3d24.'+(600+i)+'1!4d46.'+(700+i)+'2',data:''}}}}}}""")
  pg.evaluate("goV({v:'home',op:{},dr:{},q:{t:'',st:'',mo:''}})");pg.wait_for_timeout(300)
  pg.evaluate("locUpdate(null,0)");pg.wait_for_timeout(1500)
  out('after',pg.evaluate("[DB.ph.filter(needLoc).length,DB.ph.filter(p=>p.locc).length,DB.ph.find(p=>p.no=='843').locc]"))
  pg.evaluate("window.Capacitor=undefined")
  # buttons
  out('home_btns',pg.evaluate("[!!document.querySelector('.hcard [data-rtgo]'),document.querySelectorAll('#hl [data-rtgo]').length]"))
  pg.click('#hl details.mg[open] [data-rtgo]');pg.wait_for_timeout(1500)
  out('rte',pg.evaluate("[V.v,V.rts.length,V.rtgs,V.rtg]"))
  out('table',pg.evaluate("[...document.querySelectorAll('.rtt tr')].map(r=>r.innerText.replace(/\\s+/g,' '))"))
  out('links',pg.evaluate("[...document.querySelectorAll('.locs a')].map(a=>a.href.slice(0,90))"))
  # typed numbers
  pg.fill('#rtn','1184 843 99999 1136');pg.dispatch_event('#rtn','change');pg.wait_for_timeout(400)
  out('typed',pg.evaluate("[V.rts.map(id=>DB.ph.find(p=>p.id==id).no),[...document.querySelectorAll('.toast')].map(t=>t.innerText).slice(-1)]"))
  pg.evaluate("()=>{window._t=null;shareText=t=>{window._t=t}}");pg.click('[data-rtwa]');pg.wait_for_timeout(200)
  out('wa',pg.evaluate("window._t"))
  # month board button
  pg.evaluate("goV({v:'month',mo:'2026-11',op:{__rt:true},dr:{},q:{t:'',st:'',mo:''}})");pg.wait_for_timeout(300)
  out('month_rt',pg.evaluate("[document.querySelector('[data-id=__rt] summary').innerText,!!document.querySelector('[data-id=__rt] [data-rtgo]')]"))
  out('overflow',pg.evaluate("(goV({v:'rte',rts:DB.ph.map(p=>p.id),op:{},dr:{},q:V.q}),document.documentElement.scrollWidth)"))
  pg.screenshot(path=W+'t28.png',full_page=True)
  out('ERRS',E)
  br.close()

# 2.1: important places + places file, route start/return, «الموجود والناقص»
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=open(W+'bk1115/data.json',encoding='utf-8').read()
F=json.load(open(W+'out48/966-مواقع-هامة-وإحداثيات-الصيدليات-2026-11-16.json',encoding='utf-8'))
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new21.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  out=lambda k,v:print(k,'=>',v)
  out('ver',pg.evaluate("VER"))
  out('menu',pg.evaluate("MENU.map(m=>m[0]).join(',')"))
  out('needLoc before',pg.evaluate("DB.ph.filter(needLoc).map(p=>p.no)"))
  pg.evaluate("q=>plcImpOpen(q)",F);pg.wait_for_timeout(400)
  out('view',pg.evaluate("V.v"))
  out('places',pg.evaluate("[PLC().map(x=>x.ic+x.n+' '+x.c),plcHome()&&plcHome().n]"))
  out('needLoc after',pg.evaluate("DB.ph.filter(needLoc).map(p=>p.no)"))
  out('no coords',pg.evaluate("DB.ph.filter(p=>!locC(p)).map(p=>p.no)"))
  out('loc of 809/836',pg.evaluate("DB.ph.filter(p=>['809','836'].includes(p.no)).map(p=>p.no+' '+p.loc+' '+locC(p))"))
  out('plc page links',pg.evaluate("[...document.querySelectorAll('a.locb')].map(a=>a.textContent.trim()+' '+a.href)"))
  # route from the store, back to the store
  pg.evaluate("goV({v:'rte',rts:DB.ph.filter(p=>['1103','295','258'].includes(p.no)&&p.mo=='2026-11').map(p=>p.id),op:{},dr:{},q:V.q});rteGps()");pg.wait_for_timeout(500)
  out('route',pg.evaluate("(()=>{const D=rteData();return {from:D.from&&D.from.n,back:D.back&&[D.back.p.n,Math.round(D.back.d)],tot:Math.round(D.tot),order:D.rows.map(x=>x.p.no+' '+Math.round(x.d)),urls:D.parts.map(g=>rteUrl(g))}})()"))
  out('route text',pg.evaluate("rteText()"))
  out('selects',pg.evaluate("[...document.querySelectorAll('#rtsrc option,#rtret option')].map(o=>o.textContent+(o.selected?'*':'')).join(' | ')"))
  pg.select_option('#rtret','none');pg.wait_for_timeout(300)
  out('no return',pg.evaluate("(()=>{const D=rteData();return [D.back,Math.round(D.tot),D.parts.map(g=>g.length)]})()"))
  pg.select_option('#rtsrc','gps');pg.wait_for_timeout(500)
  out('gps start',pg.evaluate("[V.rtsrc,V.rtgs,(rteData().from||null)]"))
  # available / missing
  pg.evaluate("goV({v:'avl',op:{},dr:{},q:V.q})");pg.wait_for_timeout(500)
  out('avl head',pg.evaluate("document.querySelector('main').innerText.slice(0,500)"))
  R=pg.evaluate("(()=>{const D=avlData('2026-11');return D.map(o=>[o.p.no,o.need,o.have])})()")
  out('avl per pharmacy',R)
  # stock not counted twice: total taken per key never above stock
  out('double count check',pg.evaluate("""(()=>{const D=avlData('2026-11'),use={};D.forEach(o=>o.R.forEach(x=>{}));
     const st={};WU().forEach(x=>{const k=whKey0(x);st[k]=(st[k]||0)+(+x.qty||0)});
     let bad=[];const P=DB.ph.filter(p=>p.mo=='2026-11'&&p.st!='مكتملة');const tk={};
     P.sort(pSort).forEach(p=>prepRows(p).forEach(x=>{const r=x.r,need=r.cx?0:Math.max(0,qn(r)-(+r.r||0));if(!need)return;(whParts(x.t,r,p.sh)||[]).filter(y=>!y.pk&&y.f>0).forEach(y=>{const k=whKey0(y);const have=Math.min(need,Math.floor(((st[k]||0)-(tk[k]||0)+1e-9)/y.f));if(have>0)tk[k]=(tk[k]||0)+have*y.f})}));
     Object.keys(tk).forEach(k=>{if(tk[k]>(st[k]||0)+1e-9)bad.push(k)});return [Object.keys(tk).length,bad]})()"""))
  out('avl text',pg.evaluate("avlText().slice(0,400)"))
  out('stock untouched',pg.evaluate("Math.round(WU().reduce((a,x)=>a+(+x.qty||0),0)*100)/100"))
  out('errors',E);br.close()

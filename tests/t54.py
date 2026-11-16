# 2.2: invoice QR — Google code scanner first, crops for photos, tolerant parser (Capacitor mocked)
import json,base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=open(W+'bk1116/data.json',encoding='utf-8').read()
MOCK="""
window.__q={scan:[],calls:[],avail:true,img:0,imgHit:3};
const inv=(n,a)=>{const e=new TextEncoder(),P=[];[[1,n],[2,'300000000000003'],[3,'2026-11-16T07:04:00Z'],[4,a],[5,'15.00']].forEach(([t,v])=>{const b=e.encode(v);P.push(t,b.length,...b)});return btoa(String.fromCharCode(...P))};
window.__inv=inv;
window.Capacitor={isNativePlatform:()=>true,Plugins:{
 BarcodeScanner:{isSupported:async()=>({supported:true}),requestPermissions:async()=>({camera:'granted'}),
  isGoogleBarcodeScannerModuleAvailable:async()=>{__q.calls.push('avail');return {available:__q.avail}},
  installGoogleBarcodeScannerModule:async()=>{__q.calls.push('install');setTimeout(()=>__q.avail=true,2500)},
  scan:async()=>{__q.calls.push('scan');const r=__q.scan.shift();if(r instanceof Error)throw r;return r},
  addListener:async()=>({remove(){}}),removeAllListeners:async()=>{},startScan:async()=>{__q.calls.push('startScan')},stopScan:async()=>{__q.calls.push('stopScan')},
  isTorchAvailable:async()=>({available:false}),getMinZoomRatio:async()=>({zoomRatio:1}),getMaxZoomRatio:async()=>({zoomRatio:1}),
  readBarcodesFromImage:async()=>{__q.img++;__q.calls.push('img');return {barcodes:__q.img==__q.imgHit?[{rawValue:inv('محطة ساسكو','82.50')}]:[]}}},
 Filesystem:{writeFile:async()=>({uri:'file:///x.jpg'}),deleteFile:async()=>({})}}};
"""
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new22.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D)
  pg.add_init_script(MOCK);pg.reload();pg.wait_for_timeout(2500)
  out=lambda k,v:print(k,'=>',v)
  out('ver / native',pg.evaluate("[VER,CAPN(),!!MLK()]"))
  # parser
  out('parser',pg.evaluate("""(()=>{const e=new TextEncoder(),mk=(L)=>{const P=[];L.forEach(([t,v,ber])=>{const b=typeof v=='string'?e.encode(v):v;if(ber)P.push(t,0x81,b.length,...b);else P.push(t,b.length,...b)});return btoa(String.fromCharCode(...P))};
    const base=[[1,'صيدليات الدواء'],[2,'300000000000003'],[3,'2026-11-16T10:04:00'],[4,'115.00'],[5,'15.00']];
    const s=mk(base),p2=mk(base.concat([[6,new Uint8Array(32)],[8,new Uint8Array(150),1],[9,new Uint8Array(72)]])),ber2=mk([[1,'محطة'],[8,new Uint8Array(200),1],[2,'300000000000003'],[3,'2026-11-16T10:04:00'],[4,'1,150.50'],[5,'150.07']]);
    const f=x=>{const z=zatca(x);return z?[z.comp,z.vat,z.dt,z.tm,z.amt,z.tax].join('|'):null};
    return {std:f(s),urlsafe:f(s.replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'')),spaces:f(' '+s.slice(0,30)+'\\n '+s.slice(30)),phase2:f(p2),berFirst_comma:f(ber2),hex:f('0102'),junk:f('hello world')}})()"""))
  # custody page + old scanner button
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(500)
  out('buttons',pg.evaluate("[!!document.querySelector('[data-cscan]'),!!document.querySelector('[data-cscano]')]"))
  # 1) module available, scan returns an invoice
  pg.evaluate("__q.scan=[{barcodes:[{rawValue:__inv('محطة ساسكو','82.50')}]}];__q.calls=[]");pg.evaluate("cScan()");pg.wait_for_timeout(800)
  out('scan ok',pg.evaluate("[__q.calls.join(','),V.v,V.ce&&V.ce.comp,V.ce&&V.ce.amt,V.ce&&V.ce.src,!!CSC]"))
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  # 2) cancel → nothing, no fallback
  pg.evaluate("__q.scan=[new Error('scan canceled.')];__q.calls=[]");pg.evaluate("cScan()");pg.wait_for_timeout(600)
  out('cancel',pg.evaluate("[__q.calls.join(','),V.v,!!CSC]"))
  # 3) other error → old scanner
  pg.evaluate("__q.scan=[new Error('Google Play services missing')];__q.calls=[]");pg.evaluate("cScan()");pg.wait_for_timeout(900)
  out('error→old',pg.evaluate("[__q.calls.join(','),!!CSC,!!document.querySelector('.cscan')]"))
  pg.evaluate("CSC&&CSC.stop()");pg.wait_for_timeout(300)
  # 4) not an invoice, retry (dialog accepted) → second scan is an invoice
  pg.evaluate("__q.scan=[{barcodes:[{rawValue:'https://example.com'}]},{barcodes:[{rawValue:__inv('Al Dawaa','10')}]}];__q.calls=[]");pg.evaluate("cScan()");pg.wait_for_timeout(900)
  out('not invoice→retry',pg.evaluate("[__q.calls.join(','),V.v,V.ce&&V.ce.comp,V.ce&&V.ce.amt]"))
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  # 5) module missing → install → becomes available → scan
  pg.evaluate("__q.avail=false;__q.scan=[{barcodes:[{rawValue:__inv('محطة','33.10')}]}];__q.calls=[]");pg.evaluate("cScan()");pg.wait_for_timeout(6500)
  out('install',pg.evaluate("[__q.calls.filter((c,i,a)=>c!='avail'||a[i-1]!='avail').join(','),V.v,V.ce&&V.ce.amt]"))
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  # 6) old scanner button
  pg.evaluate("__q.calls=[]");pg.click('[data-cscano]');pg.wait_for_timeout(800)
  out('old button',pg.evaluate("[__q.calls.join(','),!!CSC]"));pg.evaluate("CSC&&CSC.stop()");pg.wait_for_timeout(300)
  # 7) photo: full image fails, the 2nd crop is read (3rd ML Kit call)
  A='/mnt/user-data/attachments/7db5e8a6-d495-596a-8941-a726d2c69b08/1562e1f9-image.jpg'
  b=base64.b64encode(open(A,'rb').read()).decode()
  out('photo crops',pg.evaluate("async b=>{__q.img=0;__q.calls=[];const bl=await (await fetch('data:image/jpeg;base64,'+b)).blob();const t=Date.now();const z=await qrFromBlobN(bl);return [__q.img,z&&z.comp,z&&z.amt,Date.now()-t]}",b))
  out('photo none',pg.evaluate("async b=>{__q.img=0;__q.imgHit=99;const bl=await (await fetch('data:image/jpeg;base64,'+b)).blob();const z=await qrFromBlobN(bl);return [__q.img,z]}",b))
  out('errors',E);br.close()

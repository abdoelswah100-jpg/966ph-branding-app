import sys,hashlib
from playwright.sync_api import sync_playwright
W='/home/claude/work/';F=sys.argv[1];D=open(W+'bk1106/data.json',encoding='utf-8').read()
C={'print':"V={v:'sum',sm:'print',p:DB.ph[0].id,op:{},dr:{},q:V.q};render();$('#rp')",'mgmt':"V={v:'sum',sm:'mgmt',p:DB.ph[0].id,op:{},dr:{},q:V.q};render();$('#rp')",'ck':"V={v:'sum',sm:'ck',p:DB.ph[0].id,op:{},dr:{},q:V.q};render();$('#rp')",'all':"V={v:'all',op:{},dr:{},q:V.q};render();$('#rp')",'month':"monthRepEl(DB.ph[0].mo)",'wh':"whPdfEl()"}
R={}
with sync_playwright() as pw:
  br=pw.chromium.launch()
  for th in ('light','dark'):
    pg=br.new_page(viewport={'width':400,'height':860},color_scheme=th);pg.add_init_script("(()=>{const T=new Date('2026-11-14T09:00:00').getTime(),D=Date;class F extends D{constructor(...a){super(...(a.length?a:[T]))}static now(){return T}};window.Date=F})()")
    pg.goto('file://'+W+F);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500);pg.evaluate(f"DB.cfg.th='{th}';cfg()")
    for k,ex in C.items():
      pg.evaluate(ex.rsplit(';',1)[0]) if ';' in ex else None;pg.wait_for_timeout(400)
      b=pg.evaluate("async ex=>{const L=pdfLayout(eval(ex),'t');const o=[];try{for(const p of L.pages){const m=await pgJpeg(p,1);o.push(Array.from(m.b.slice(0,0)).length+m.b.length+':'+[...m.b].reduce((a,x,i)=>(a*31+x)%1000000007,7))}}finally{L.host.remove()}return o.join(',')}",ex)
      R.setdefault(k,[]).append(b)
    pg.close()
  br.close()
for k,v in R.items():print(k,'SAME' if v[0]==v[1] else 'DIFF',v)

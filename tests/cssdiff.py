# Compare computed styles of every element on key screens between two builds.
import sys, json
from playwright.sync_api import sync_playwright
W='/home/claude/work/'; A,B=sys.argv[1],sys.argv[2]
DATA=open(W+'out6/966-data-v1.2.json',encoding='utf-8').read()
VIEWS=["V={v:'home',op:{},dr:{},q:{t:'',st:'',mo:''}}","V={v:'ph',p:DB.ph[0].id,op:{ws:true,wh:true,fh:true},dr:{},q:V.q}",
"V={v:'sum',sm:'sum',p:DB.ph[0].id,op:{},dr:{},q:V.q}","V={v:'sum',sm:'ck',p:DB.ph[0].id,op:{},dr:{},q:V.q}",
"V={v:'exec',p:DB.ph[0].id,op:{},dr:{},q:V.q}","V={v:'nq',nk:'x',ns:'ph',p:DB.ph[0].id,mo:DB.ph[0].mo,op:{},dr:{},q:V.q}",
"V={v:'all',op:{},dr:{},q:V.q}","V={v:'bk',op:{},dr:{},q:V.q}","V={v:'gen',op:{},dr:{},q:V.q}","V={v:'revhub',op:{},dr:{},q:V.q}"]
JS="""()=>[...document.querySelectorAll('body *')].filter(e=>!e.closest('.toast')).map(e=>{const c=getComputedStyle(e);return e.tagName+'.'+e.className+'|'+['color','background-color','font-weight','font-size','opacity','display','padding','margin','border','width','height'].map(k=>c[k]).join(',')})"""
def run(f,dark):
    out={}
    with sync_playwright() as pw:
        br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg=br.new_page(viewport={'width':400,'height':860})
        pg.goto('file://'+W+f);pg.wait_for_timeout(300)
        pg.evaluate("d=>localStorage.setItem('ads',d)",DATA);pg.reload();pg.wait_for_timeout(1800)
        # mark some receipt/execution counts so row colours show
        pg.evaluate("(()=>{const p=DB.ph[0];Object.values(p.rows).forEach(a=>Array.isArray(a)&&a.forEach((r,i)=>{r.r=i%3==0?qn(r):i%3==1?Math.min(1,qn(r)-1):0;r.x=i%2?qn(r):0}));if("+('true' if dark else 'false')+")document.documentElement.dataset.th='dark';})()")
        for v in VIEWS:
            pg.evaluate(v+";render()");pg.wait_for_timeout(250)
            out[v[:40]]=pg.evaluate(JS)
        br.close()
    return out
for dark in (False,True):
    a,b=run(A,dark),run(B,dark)
    for k in a:
        if a[k]!=b[k]:
            d=[(x,y) for x,y in zip(a[k],b[k]) if x!=y]
            print('DIFF',('dark ' if dark else '')+k,len(a[k]),len(b[k]),d[:3])
        else: print('same',('dark ' if dark else '')+k,len(a[k]))

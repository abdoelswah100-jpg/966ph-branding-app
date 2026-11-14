# contrast audit: every text element on every screen, light + dark
import json,sys,collections
from playwright.sync_api import sync_playwright
W='/home/claude/work/';F=sys.argv[1];OUT=sys.argv[2]
D=open(W+'bk1106/data.json',encoding='utf-8').read()
VIEWS='add all atb bk calc cdoc ced cust docs exec gd gen home imgs imp imr inv lang lockset look mclose med mnt month mrb nq ntf ph prc prep qe rca rcv req reqe rev revhub rte rto set sum sync types ued usr wh wha whe who whr wht wlog xr'.split()
EXTRA={'ph':"op:{ws:true,wh:true,fh:true,ec:true,eg:true,md:true,ga:true}",'sum':"sm:'sum'",'nq':"nk:'x',ns:'ph',mo:DB.ph[0].mo"}
JS=r"""()=>{const P=s=>{const m=s.match(/[\d.]+/g);return m?m.map(Number):null};
const L=c=>{c=c/255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4)},Y=a=>.2126*L(a[0])+.7152*L(a[1])+.0722*L(a[2]);
const bgOf=e=>{let rgb=null,grad=false;for(let x=e;x;x=x.parentElement){const c=getComputedStyle(x);if(c.backgroundImage&&c.backgroundImage.includes('gradient')){grad=c.backgroundImage.slice(0,60);const m=P(c.backgroundImage);return {rgb:m?m.slice(0,3):null,grad}}if(/color\(/.test(c.backgroundColor))return {rgb:null};const b=P(c.backgroundColor);if(b&&(b.length<4||b[3]>.5))return {rgb:b.slice(0,3),grad:false}}return {rgb:[255,255,255],grad:false}};
const o=[];document.querySelectorAll('body *').forEach(e=>{if(!e.offsetParent&&getComputedStyle(e).position!='fixed')return;const t=[...e.childNodes].filter(n=>n.nodeType==3&&n.textContent.trim()).map(n=>n.textContent.trim()).join(' ');if(!t)return;
 const c=getComputedStyle(e);if(c.visibility=='hidden'||+c.opacity<.2)return;const f=P(c.color);if(!f)return;const b=bgOf(e);if(!b.rgb)return;
 const y1=Y(f),y2=Y(b.rgb),r=(Math.max(y1,y2)+.05)/(Math.min(y1,y2)+.05),big=parseFloat(c.fontSize)>=18.6||(parseFloat(c.fontSize)>=14&&+c.fontWeight>=700);
 if(r<(big?3:4.5))o.push({r:Math.round(r*100)/100,fg:c.color,bg:'rgb('+b.rgb.join(',')+')',grad:!!b.grad,cls:e.tagName.toLowerCase()+(e.className&&typeof e.className=='string'?'.'+e.className.trim().split(/\s+/).join('.'):''),par:(e.parentElement&&typeof e.parentElement.className=='string'?e.parentElement.className.split(' ')[0]:''),t:t.slice(0,40),fs:c.fontSize})});return o}"""
res={}
with sync_playwright() as pw:
  br=pw.chromium.launch()
  for mode in ('L','D','F'):
    dark=mode!='L'
    pg=br.new_page(viewport={'width':400,'height':860},color_scheme='dark' if dark else 'light');pg.on('dialog',lambda x:x.dismiss())
    pg.goto('file://'+W+F);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
    pg.evaluate("(()=>{const p=DB.ph[0];Object.values(p.rows).forEach(a=>Array.isArray(a)&&a.forEach((r,i)=>{r.r=i%3==0?qn(r):i%3==1?Math.min(1,qn(r)-1):0;r.x=i%2?qn(r):0}))})()");pg.evaluate("m=>{DB.cfg.th=m=='F'?'dark':'';cfg()}",mode)
    pg.evaluate("w=>{DB.wh=w;sv()}",json.load(open(W+'jard/966-مخزن-هيدر-جندولة-2026-11-14.json'))['items'][:8]+[dict(x,id=900+i,min=5) for i,x in enumerate(json.load(open(W+'jard/966-مخزن-جرد-End-cap-وأجواء-صيفية-2026-11-14.json'))['items'][:6])])
    for v in VIEWS+['IMPORT','TOAST']:
      try:
        pg.evaluate("document.querySelectorAll('.csh,.toast').forEach(e=>e.remove())")
        if v=='IMPORT':pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.evaluate("q=>whImpOpen(q,'x.json')",json.load(open(W+'t48_wh.json')))
        elif v=='TOAST':pg.evaluate("goV({v:'ph',p:DB.ph[0].id,op:{},dr:{},q:V.q});toastT('تجربة');toast('<span>نص <b>عريض</b></span><button class=pr>زرار</button><button>لا</button>')")
        else:pg.evaluate(f"V={{v:'{v}',p:DB.ph[0].id,{EXTRA.get(v,'op:{}')},op:V.op||{{}},dr:{{}},q:V.q}};render()") if v in EXTRA else pg.evaluate(f"V={{v:'{v}',p:DB.ph[0].id,op:{{}},dr:{{}},q:V.q}};render()")
        pg.wait_for_timeout(350);res[mode+' '+v]=pg.evaluate(JS)
      except Exception as e:res[mode+' '+v]=[{'err':str(e)[:100]}]
    pg.close()
  br.close()
json.dump(res,open(OUT,'w'),ensure_ascii=False,indent=0)
agg=collections.defaultdict(lambda:[0,set(),'',9])
for k,L in res.items():
  for x in L:
    if 'err' in x:print('ERR',k,x['err']);continue
    a=agg[(k[0],x['fg'],x['bg'],x['cls'])];a[0]+=1;a[1].add(k[2:]);a[2]=a[2] or x['t'];a[3]=min(a[3],x['r'])
for (m,fg,bg,cls),(n,vs,t,r) in sorted(agg.items(),key=lambda kv:(kv[0][0],kv[1][3])):print(m,r,fg,'on',bg,cls,n,sorted(vs)[:6],t)
print('TOTAL',len(agg),{m:sum(1 for k in agg if k[0]==m) for m in 'LDF'})

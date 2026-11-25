# regression without the old fixtures: same data (backups 15-11 and 16-11) in two builds, every screen's text + key functions
import json,sys,difflib
from playwright.sync_api import sync_playwright
W='/home/claude/work/';A,B=sys.argv[1],sys.argv[2]
DATA=[('bk1125',W+'bk1125/data.json'),('bk1123',W+'bk1123/data.json'),('bk1116',W+'bk1116/data.json'),('bk1115','/mnt/user-data/attachments/7db5e8a6-d495-596a-8941-a726d2c69b08/b536172f-966-backup-2026-11-15.json')]
VIEWS=["{v:'home'}","{v:'sum'}","{v:'mo'}","{v:'wh'}","{v:'rcv'}","{v:'prep'}","{v:'avl'}","{v:'cust'}","{v:'mnt'}","{v:'set'}","{v:'rte'}","{v:'plc'}"]
def grab(f,data):
  o={}
  with sync_playwright() as pw:
    br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
    pg.goto('file://'+W+f);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",data);pg.reload();pg.wait_for_timeout(3000)
    for v in VIEWS:
      try:pg.evaluate(f"goV(Object.assign({v},{{op:{{}},dr:{{}},q:V.q}}))");pg.wait_for_timeout(400);o['view '+v]=pg.evaluate("document.querySelector('#app').innerText")
      except Exception as e:o['view '+v]='ERR '+str(e)[:80]
    ids=pg.evaluate("DB.ph.map(p=>p.id)")
    for i in ids:
      try:pg.evaluate(f"goV({{v:'ph',p:{i},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(120);o[f'ph {i}']=pg.evaluate("document.querySelector('#app').innerText")
      except Exception as e:o[f'ph {i}']='ERR'
    o['fn']=pg.evaluate("""JSON.stringify(DB.ph.map(p=>({no:p.no,mo:p.mo,nq:nqLines(p,'r').map(x=>[x.nm,x.pt,x.sz,x.d]),sur:whSurplus(p),cap:[capN(p,'q'),capN(p,'x')],prep:prepRows(p).length})))""")
    o['errors']=json.dumps(E);br.close()
  return o
for name,path in DATA:
  r=json.load(open(path,encoding='utf-8'));d=r.get('data',r) if isinstance(r,dict) else r
  data=json.dumps(d if not isinstance(d,str) else json.loads(d),ensure_ascii=False)
  a,b=grab(A,data),grab(B,data);same=0
  for k in a:
    if a[k]==b.get(k):same+=1;continue
    print(f'== {name} DIFF {k}')
    for l in list(difflib.unified_diff(a[k].splitlines(),b.get(k,'').splitlines(),lineterm='',n=0))[2:14]:print('   ',l[:220])
  print(f'{name}: same {same} / {len(a)}')

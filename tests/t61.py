# 3.2 on the 27-11 backup: every new item, widths 360, no page errors
import json,base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.load(open(W+'bk1127/raw.json',encoding='utf-8'))
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch()
  def boot(data,w=360):
    c=br.new_context(viewport={'width':w,'height':800});pg=c.new_page();E=[];M=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:(M.append(x.message[:300]),x.accept()))
    pg.goto('file://'+W+'new32.html');pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(data,ensure_ascii=False));pg.reload();pg.wait_for_timeout(3500);return pg,E,M
  pg,E,M=boot(D);R=lambda js,a=None:pg.evaluate(js,a) if a is not None else pg.evaluate(js)
  wid=lambda:R("[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
  out('ver/title',[R("VER"),R("document.title")]);out('c32',R("JSON.stringify(DB.cfg.c32)"))
  out('min set / jd items',R("[WU().filter(x=>+x.min==3).length,WU().filter(x=>x.jd).length]"))
  out('FH big per shelf',R("[0,1,3,4].map(s=>T.find(t=>t.id=='fh').z({sec:'Health',nm:'Strong H Vitamins',sz:'كبير',q:1},s))"))
  out('EG Baby big parts',R("JSON.stringify(whParts(T.find(t=>t.id=='eg'),{nm:'Baby (Big) · Body care · نهتم بطفلك',sz:'كبير',q:1},0).map(y=>[y.ty,y.nm,y.size]))"))
  out('EG baby big side qty',R("whQty(whParts(T.find(t=>t.id=='eg'),{nm:'Baby (Big) · Body care · نهتم بطفلك',sz:'كبير',q:1},0).find(y=>/Side/.test(y.ty)))"))
  # pharmacies of the open months
  out('months',R("JSON.stringify([...new Set(DB.ph.map(p=>p.mo+':'+p.st))])"))
  # per-type pull candidates
  cand=R("JSON.stringify(DB.ph.filter(p=>p.st!='مكتملة'&&uEditP(p)).map(p=>[p.no,p.mo,TY(p).map(t=>{const n=tpUsed(p,t.id).reduce((a,u)=>a+u.n+(u.np||0),0);return n?t.id+':'+n:''}).filter(Boolean).join(',')]).filter(x=>x[2]))")
  out('tp candidates',cand);C=json.loads(cand)
  if C:
    no,mo,s=C[0];tid=s.split(',')[0].split(':')[0]
    R("a=>{const p=DB.ph.find(p=>p.no==a[0]&&p.mo==a[1]);goV({v:'ph',p:p.id,op:{[a[2]]:true},dr:{},q:V.q})}",[no,mo,tid]);pg.wait_for_timeout(500)
    out('tp button',R("[...document.querySelectorAll('[data-tp32]')].map(b=>b.innerText)"));out('width ph',wid())
    before=R("WU().reduce((a,x)=>a+(+x.qty||0),0)")
    R("t=>v24Click({tp32:t},document.body)",tid);pg.wait_for_timeout(500)
    out('tp pulled (stock delta)',before-R("WU().reduce((a,x)=>a+(+x.qty||0),0)"));out('dialog',M[-1][:200] if M else '')
  # spare on a fully received row with stock
  sp=R("""JSON.stringify((()=>{for(const p of DB.ph){if(p.st=='مكتملة'||!uEditP(p))continue;for(const t of TY(p)){const rs=p.rows[t.id]||[];for(let i=0;i<rs.length;i++){const r=rs[i];if(!r.cx&&qn(r)>0&&spAv(p,t,r)>0)return [p.id,t.id,i]}}}return null})())""")
  out('spare cand',sp)
  if sp!='null':
    pid,tid,i=json.loads(sp)
    R("a=>goV({v:'ph',p:a[0],op:{[a[1]]:true},dr:{},q:V.q})",[pid,tid]);pg.wait_for_timeout(400)
    R("a=>{const p=curP();whFrom(p,T.find(t=>t.id==a[1]),p.rows[a[1]][a[2]],a[2])}",[pid,tid,i]);pg.wait_for_timeout(300)
    out('toast',R("(document.querySelector('.toast .sp32')||{}).innerText"));out('width toast',wid())
    q0=R("a=>{const p=curP();return spAv(p,T.find(t=>t.id==a[1]),p.rows[a[1]][a[2]])}",[pid,tid,i])
    R("a=>{const b=document.querySelector('[data-sp32]');v24Click(b.dataset,b)}",[pid,tid,i]);pg.wait_for_timeout(300)
    out('after spare: wz / avail before→after',R("a=>{const p=curP(),r=p.rows[a[1]][a[2]];return [r.wz,spAv(p,T.find(t=>t.id==a[1]),r)]}",[pid,tid,i]),);out('avail before',q0)
    out('row tag',R("(document.querySelector('.spt')||{}).innerText"))
    out('surplus has spare',R("JSON.stringify(Object.values(whSurplus(curP())).filter(x=>(x.why||[]).includes('احتياطي')).map(x=>[x.ty,x.nm,x.q]))"))
    R("a=>{const p=curP();whFrom(p,T.find(t=>t.id==a[1]),p.rows[a[1]][a[2]],a[2])}",[pid,tid,i]);pg.wait_for_timeout(300)
    R("()=>{const b=document.querySelector('[data-spb32]');v24Click(b.dataset,b)}");pg.wait_for_timeout(300)
    out('after back',R("a=>{const p=curP(),r=p.rows[a[1]][a[2]];return [r.wz,spAv(p,T.find(t=>t.id==a[1]),r)]}",[pid,tid,i]))
  # earlier-pharmacies warning
  ew=R("JSON.stringify(DB.ph.filter(p=>p.st!='مكتملة').map(p=>{const e=avlEarlier(p);return e?[p.no,p.mo,e.lost,e.who.join('،')]:null}).filter(Boolean))")
  out('earlier warn',ew)
  # duplicate guard: a completed pharmacy that was transferred, whT dropped
  dp=R("JSON.stringify(DB.ph.filter(p=>p.whT&&Object.keys(p.whT).length).map(p=>[p.id,p.no,p.mo,Object.keys(p.whT).length]))");out('transferred',dp)
  for pid,no,mo,n in json.loads(dp)[:3]:
    R("id=>{const p=DB.ph.find(p=>p.id==id);V.p=p.id;p._w=p.whT;p.whT={};goV({v:'wht',p:p.id,op:{},dr:{},q:V.q})}",pid);pg.wait_for_timeout(300)
    b0=R("WU().reduce((a,x)=>a+(+x.qty||0),0)");plan=R("whPlan(curP()).reduce((a,x)=>a+x.dl,0)");nm=len(M)
    R("whApply()");pg.wait_for_timeout(300)
    out('dup '+no+' '+mo,[plan,R("WU().reduce((a,x)=>a+(+x.qty||0),0)")-b0,(M[-1][:160] if len(M)>nm else 'no dialog')])
  # stock-take sheet: wrong section + last count date
  R("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  f=W+'jard/t61.json';json.dump({"kind":"966-warehouse","mode":"set","items":[{"ty":"Floor Header","sh":1,"sec":"Beauty","nm":"Professional Hair Care","size":"14×59","mat":"باك لايت","qty":1},{"ty":"Floor Header","sh":1,"sec":"Personal","nm":"Cleansers & Moisturizers","size":"14×59","mat":"باك لايت","qty":1}]},open(f,'w',encoding='utf-8'),ensure_ascii=False)
  pg.set_input_files('#imp',f);pg.wait_for_timeout(1200)
  out('sheet warn',R("[...document.querySelectorAll('.csh .alr, .csh .c-exp')].map(x=>x.innerText).filter(t=>/قسم/.test(t))"));out('width sheet',wid())
  R("v24Click({jrd31:1},document.body)");pg.wait_for_timeout(600)
  out('jd stamped',R("JSON.stringify(WU().filter(x=>x.ty=='Floor Header'&&/Professional Hair|Cleansers/.test(x.nm)&&x.sh==1).map(x=>[x.sec,x.nm,x.qty,(x.jd||'').slice(0,10)]))"))
  # warehouse screen + card date + movement
  R("goV({v:'wh',op:{},dr:{},q:V.q,wf:{sh:''}})");pg.wait_for_timeout(500)
  out('wh buttons',R("[...document.querySelectorAll('.cbtn button')].map(b=>b.innerText)"));out('width wh',wid())
  out('card jd',R("[...document.querySelectorAll('.whc .mu')].map(x=>x.innerText).filter(t=>/آخر جرد/.test(t)).slice(0,2)"))
  R("v24Click({wm32:1},document.body)");pg.wait_for_timeout(500)
  out('movement head',R("(document.querySelector('.csh small')||{}).innerText"));out('width movement',wid())
  out('movement rows / tot',R("[document.querySelectorAll('.csh .wm32 tr').length,(document.querySelector('.csh .wm32 tr.tot')||{}).innerText]"))
  b64=R("async()=>{const bl=rpXlsx(wmEl(WM32).el);const a=new Uint8Array(await bl.arrayBuffer());let s='';for(let i=0;i<a.length;i+=8192)s+=String.fromCharCode.apply(null,a.subarray(i,i+8192));return btoa(s)}")
  open(W+'m29/wm32.xlsx','wb').write(base64.b64decode(b64));out('xlsx bytes',len(base64.b64decode(b64)))
  R("cShClose();goV({v:'set'})");pg.wait_for_timeout(400);out('settings fh.ln',R("[...document.querySelectorAll('[data-sk=\"fh.ln\"]')].map(x=>x.value)"));out('width set',wid())
  out('errors',E)
  br.close()

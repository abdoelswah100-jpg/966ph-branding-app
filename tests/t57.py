# 2.6 on the 23-11 backup (+ the 2.5 files): every item, widths 360/400, no page errors
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';O='/mnt/user-data/outputs/';D=json.load(open(W+'bk1123/data.json',encoding='utf-8'))
J=lambda f:json.load(open(O+f,encoding='utf-8'))
def run(pg,js,a=None):return pg.evaluate(js,a) if a is not None else pg.evaluate(js)
def wid(pg):return run(pg,"[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':360,'height':800});E=[];M=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:(M.append(x.message[:120]),x.accept()))
  out=lambda k,v:print(k,'=>',v)
  pg.goto('file://'+W+'new26.html');pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(3500)
  out('ver',run(pg,"VER"));out('restore point',run(pg,"snaps().map(x=>x.why).slice(0,3)"))
  out('neg fixed',run(pg,"WU().filter(x=>+x.qty<0).length"))
  run(pg,"q=>holdImp(q)",J('966-تحت-الانتظار-صيانة-Riyadh2-26.json'));run(pg,"q=>phImpGo(q,'fix')",J('966-تصحيح-تبديل-674-695.json'));pg.wait_for_timeout(300)
  M.clear();run(pg,"q=>phImpGo(q,'fix')",J('966-تصحيح-تبديل-674-695.json'));out('repeat warning',[m for m in M if 'اتدخل قبل كده' in m][:1])
  run(pg,"q=>plcImpOpen(q)",J('966-مواقع-وأرقام-هامة-2.6.json'));pg.wait_for_timeout(500)
  out('places order',run(pg,"PLC().map(x=>x.n+(x.wa?' 💬':'')+(x.tel?' 📞':''))"));out('contacts',run(pg,"CNT().length"));out('width plc',wid(pg))
  run(pg,"v24Click({gov:'cnt'},document.body)");pg.wait_for_timeout(400);out('cnt view',[run(pg,"document.querySelectorAll('.cnt26').length"),run(pg,"document.querySelector('a[href^=\"https://wa.me/966\"]')?.href"),wid(pg)])
  out('menu',run(pg,"MENU.map(m=>m[0]+':'+String(m[1]).replace(/<[^>]+>/g,'')).join(' | ')"))
  # 1 + 2
  out('ab total 510',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11');const h=mgmtHtml(p),m=h.match(/إجمالي Acrylic boards<\\/td><td>([^<]*)/);return m&&m[1]})()"))
  out('progress no nails 695',run(pg,"(p=>[tkProg(p,'x').n,nailN(p)])(DB.ph.find(p=>p.no=='695'&&p.mo=='2026-11'))"))
  # 4
  out('whAdd clamp',run(pg,"(()=>{const x=WU().find(y=>+y.qty>0&&y.ty=='End cap');const q=+x.qty;whAdd(x,-(q+3),'out','t','t');const r=[q,+x.qty,DB.wlog[0].note];whAdd(x,q,'in','t','undo');return r})()"))
  # 5
  run(pg,"goV({v:'chk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(400);out('chk',run(pg,"chkList().map(x=>x.g).reduce((a,g)=>(a[g]=(a[g]||0)+1,a),{})"));out('width chk',wid(pg))
  # 6 load list
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='674'&&p.mo=='2026-11');p.ds='2026-11-23';p.de='2026-11-24';p.st='جاري'})()")
  run(pg,"goV({v:'load',op:{},dr:{},q:V.q,ld:'2026-11-24'})");pg.wait_for_timeout(500)
  out('load',run(pg,"ldData('2026-11-24').map(o=>o.p.no+' need'+o.need+' have'+o.have)"));out('chips',run(pg,"[...document.querySelectorAll('.chip26 button')].map(b=>b.textContent).join('|')"));out('width load',wid(pg))
  out('load pull',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='674'&&p.mo=='2026-11'),r=p.rows.saf.find(r=>r.xi);const b=[r.r||0];ldGo('all');return b.concat([r.r||0,(DB.wlog[0]||{}).note])})()"))
  # 7 Khobar
  run(pg,"goV({v:'kbr',op:{},dr:{},q:V.q,am2:'2026-11'})");pg.wait_for_timeout(500);out('kbr',[run(pg,"kbData('2026-11').length"),run(pg,"kbText('new').split('\\n').slice(0,4).join(' / ')")]);out('width kbr',wid(pg))
  run(pg,"v24Click({kbok:1},document.body)");out('kbr marked',run(pg,"Object.keys(kbM()).length"))
  # 8 tools on completion
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='695'&&p.mo=='2026-11');V.p=p.id;p.st='مكتملة';whOffer(p,true)})()");pg.wait_for_timeout(400)
  out('tools sheet',run(pg,"document.querySelectorAll('.tlg button').length"));out('width tools',wid(pg))
  run(pg,"v24Click({tlok:1},document.body)");pg.wait_for_timeout(400);out('then complete sheet',run(pg,"!!document.querySelector('[data-cpx]')"))
  # 13 rolls
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11');goV({v:'ph',p:p.id,op:{ws:true},dr:{},q:V.q})})()");pg.wait_for_timeout(500)
  out('roll line',run(pg,"document.querySelector('.rlx26 summary')?.textContent"));out('width ph',wid(pg))
  out('roll deduct',run(pg,"(()=>{const p=curP();whAdd({sh:-1,ty:RLTY,nm:'تخطيط',sec:'Beauty',mat:'',size:'عرض 1 م'},50,'in','t','t');const r=p.rows.ws.find(r=>r.kd=='تخطيط'&&r.sec=='Beauty');if(!r)return 'no row';const st0=rlStockOf({nm:'تخطيط',sec:'Beauty'});r.x=(+r.x||0)>0?0:(+r.q||1);sv();const st1=rlStockOf({nm:'تخطيط',sec:'Beauty'});return [r.h,r.w,r.q,r.x,st0,st1]})()"))
  # settings & types
  run(pg,"goV({v:'gen',op:{__s_tl:true,__s_vz:true,__s_ck:true},dr:{},q:V.q})");pg.wait_for_timeout(500);out('gen sections',run(pg,"document.querySelectorAll('[data-c26],[data-c26v],[data-c26m]').length"));out('width gen',wid(pg))
  run(pg,"(()=>{const t=document.querySelector('[data-c26=\"tools\"]');t.value='كاتر\\nمتر';t.dispatchEvent(new Event('change',{bubbles:true}))})()");out('tools saved',run(pg,"TOOLS()"))
  run(pg,"(()=>{const t=document.querySelector('[data-c26=\"ck\"]');t.value=t.value+'\\nإكراميات: إكرامية عامل';t.dispatchEvent(new Event('change',{bubbles:true}))})()");out('custody kinds',[run(pg,"CK.slice(-2)"),run(pg,"descOf('إكراميات','10:00','x')"),run(pg,"descOf('عمالة','10:00','x')")])
  out('VZ',run(pg,"[VZ.h0,VZ.out]"))
  run(pg,"goV({v:'tab',op:{},dr:{},q:V.q})");pg.wait_for_timeout(400);out('width tab',wid(pg))
  run(pg,"(()=>{$('#abxn').value='لوحة عروض';$('#abxs').value='40×60';v24Click({abxa:1},document.body)})()");out('new ab item',run(pg,"[ABI.includes('لوحة عروض'),SZ('abs.لوحة عروض')]"))
  out('ABD default edit',run(pg,"(()=>{V.op['abd_تعديل براندنج']=true;render();const m='تعديل براندنج';const n0=ABD(m).length;v24Click({abdd:m+'|0'},document.body);return [n0,ABD(m).length]})()"))
  for v in ['tlr','tmw','tfr','types','set','imgs','prc','bk']:
    run(pg,f"goV({{v:'{v}',op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(400);out('width '+v,[wid(pg),run(pg,"!!document.querySelector('.chip26')")])
  out('bk groups',run(pg,"[...document.querySelectorAll('.bkg26>summary')].map(s=>s.textContent)"))
  pg.set_viewport_size({'width':400,'height':800});pg.wait_for_timeout(300);out('width 400 bk',wid(pg))
  out('errors',E);br.close()

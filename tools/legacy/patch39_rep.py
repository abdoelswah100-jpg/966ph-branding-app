"""v1.9 part 3: start / end dates per pharmacy in the management reports, executed raises received (+ migration),
app version in backups (shown on restore), month-close checklist."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'mcloseHtml' not in s
# dates per pharmacy
JS = r"""// start / end dates of every pharmacy (management reports)
const ddm=d=>d?d.split('-').reverse().join('-'):'—';
const phDates=P=>P.length?`<h3>تواريخ الصيدليات</h3><div class="sc"><table><tr><th>الصيدلية</th><th>الحي</th><th>تاريخ البدء</th><th>تاريخ الانتهاء</th><th>الحالة</th></tr>${P.slice().sort(pSort).map(p=>`<tr><td><b>${esc(p.no)}</b></td><td>${esc(p.name||'—')}</td><td>${ddm(p.ds)}</td><td>${ddm(p.de)}</td><td style="background:${SC[p.st]||'#7A8699'};color:#fff;font-weight:700">${esc(p.st||'')}</td></tr>`).join('')}</table></div>`:'';
// month close: what is still open for the month
function mcloseHtml(){const m=V.mo||MN(),L=DB.ph.filter(p=>p.mo==m).sort(pSort),C=CU(),M=C.m[m],sec=(t,ok,rows)=>`<div class="wcard mcl${ok?' ok':''}"><h3>${ok?'✅':'⚠'} ${t}</h3>${ok?'<small>تمام</small>':rows}</div>`,ln=(a,txt)=>`<button class="mcr" ${a}>${txt} ›</button>`;
 const nc=L.filter(p=>p.st!='مكتملة'),sp=L.filter(p=>p.st=='مكتملة'&&whPlan(p).length),nx=L.filter(p=>nqLines(p,'x').length),nr=L.filter(p=>nqLines(p,'r').length),rv=L.filter(p=>revSt(p)!='ok');
 return `<div class="wcard"><h2>${ic('check')}إقفال شهر ${m.slice(5)}-${m.slice(0,4)}</h2><p class="sub">اللي فاضل قبل ما تقفل الشهر. اضغط على أي سطر يوديك له.</p></div>`
 +sec('صيدليات لسه مش مكتملة ('+nc.length+')',!nc.length,nc.map(p=>ln(`data-go="${p.id}"`,`صيدلية ${esc(p.no)} · ${esc(p.st||'لم تبدأ')}`)).join(''))
 +sec('فائض ما اترحّلش للمخزن ('+sp.length+')',!sp.length,sp.map(p=>ln(`data-whdone="${p.id}"`,`صيدلية ${esc(p.no)} · ${whPlan(p).length} صنف`)).join(''))
 +sec('نواقص التنفيذ ('+nx.length+')',!nx.length,nx.map(p=>ln(`data-mcnq="x:${p.id}"`,`صيدلية ${esc(p.no)} · ${nqLines(p,'x').reduce((a,y)=>a+y.d,0)} قطعة`)).join(''))
 +sec('نواقص الطباعة ('+nr.length+')',!nr.length,nr.map(p=>ln(`data-mcnq="r:${p.id}"`,`صيدلية ${esc(p.no)} · ${nqLines(p,'r').reduce((a,y)=>a+y.d,0)} قطعة`)).join(''))
 +sec('المراجعة ('+rv.length+')',!rv.length,rv.map(p=>ln(`data-go="${p.id}"`,`صيدلية ${esc(p.no)} · ${revSt(p)=='old'?'مراجعة قديمة':'ما اتراجعتش'}`)).join(''))
 +sec('العهدة',!!(M&&M.xat&&M.items.length),M&&M.items.length?ln('data-tab="cust"',M.xat?`آخر تصدير ${fd(M.xat)} · فيه تعديل بعده؟ صدّر تاني`:`${M.items.length} فاتورة · لسه ما اتصدّرتش Excel / PDF`):'<small>مفيش فواتير للشهر ده</small>')}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("DB.dt.rr||[]}):V.am=='sz'", "DB.dt.rr||[]})+phDates(P):V.am=='sz'")
rep("th(['الصيدلية','الحي','المنطقة','الرفوف','التعديل','الحالة','المراجعة','البنود','Wall Sticker م²'])}<tbody>${L.map(p=>`<tr><td>${esc(p.no)}</td><td>${esc(p.name||'—')}</td>", "th(['الصيدلية','الحي','البدء','الانتهاء','المنطقة','الرفوف','التعديل','الحالة','المراجعة','البنود','Wall Sticker م²'])}<tbody>${L.map(p=>`<tr><td>${esc(p.no)}</td><td>${esc(p.name||'—')}</td><td>${ddm(p.ds)}</td><td>${ddm(p.de)}</td>")
# month close: button + screen + custody export time
rep("<button class=\"b-wa\" data-mshare=\"1\">", "<button class=\"b-wa\" data-mcls=\"1\" style=\"background:#1E7B45\">${ic('check')}إقفال الشهر</button><button class=\"b-wa\" data-mshare=\"1\">")
rep(" if(d.mshare){", " if(d.mcls&&V.v=='month'){goV({v:'mclose',mo:V.mo,op:{},dr:{},q:V.q});return}\n if(d.mcnq){const[k,id]=d.mcnq.split(':');goV({v:'nq',nk:k,ns:'ph',p:+id,from:'mclose',op:{},dr:{},q:V.q,mo:V.mo});return}\n if(d.mshare){")
rep(" if(V.v=='month'){", " if(V.v=='mclose'){a.innerHTML=hdr('<button data-tab=\"month\">‹ لوحة الشهر</button>','إقفال الشهر')+`<main>${mcloseHtml()}</main>`;return}\n if(V.v=='month'){")
rep("async function cExport(kind,mode){const k=CU().cur;", "async function cExport(kind,mode){const k=CU().cur;if(CU().m[k]){CU().m[k].xat=nowIso();svq()}")
# executed raises received
rep("function tkSet(p,k,tid,i,v){const r=p.rows[tid]&&p.rows[tid][+i];if(!r)return;const pk=k.length==3,q=pk?egN(r,p.sh,k[2]):qn(r);v=Math.max(0,Math.round(+v||0));r[k]=v;{const rv=pk?pkv(r,'r',k[2]):(+r.r||0);if(k[0]=='x'&&v>rv)toastT('⚠ المتنفذ ('+v+') أكتر من المستلم من الطباعة ('+rv+')')}",
    "function tkSet(p,k,tid,i,v){const r=p.rows[tid]&&p.rows[tid][+i];if(!r)return;const pk=k.length==3,q=pk?egN(r,p.sh,k[2]):qn(r);v=Math.max(0,Math.round(+v||0));r[k]=v;{const rk=pk?'rp'+k[2]:'r',rv=+r[rk]||0;if(k[0]=='x'&&v>rv){r[rk]=v;toastT('✓ المستلم اتعدّل لـ '+v+' (المتنفذ لازم يكون مستلم)')}}")
rep("else if(d.tkt){const[k,tid]=d.tkt.split(':');(p.rows[tid]||[]).forEach((r,i)=>{if(qn(r)>0)r[k]=qn(r);", "else if(d.tkt){const[k,tid]=d.tkt.split(':');(p.rows[tid]||[]).forEach((r,i)=>{if(qn(r)>0){r[k]=qn(r);if(k=='x'&&(+r.r||0)<qn(r))r.r=qn(r)}")
rep("else if(d.tkall){ckRows(p).forEach(x=>{x.r[d.tkall]=qn(x.r);", "else if(d.tkall){ckRows(p).forEach(x=>{x.r[d.tkall]=qn(x.r);if(d.tkall=='x'&&(+x.r.r||0)<qn(x.r))x.r.r=qn(x.r);")
rep("if(tid=='eg'&&egSub(r,p.sh))SDS.forEach(([sd])=>r[k+'p'+sd]=egN(r,p.sh,sd))", "if(tid=='eg'&&egSub(r,p.sh))SDS.forEach(([sd])=>{r[k+'p'+sd]=egN(r,p.sh,sd);if(k=='x')r['rp'+sd]=Math.max(+r['rp'+sd]||0,egN(r,p.sh,sd))})")
rep("if(x.t.id=='eg'&&egSub(x.r,p.sh))SDS.forEach(([sd])=>x.r[d.tkall+'p'+sd]=egN(x.r,p.sh,sd))", "if(x.t.id=='eg'&&egSub(x.r,p.sh))SDS.forEach(([sd])=>{x.r[d.tkall+'p'+sd]=egN(x.r,p.sh,sd);if(d.tkall=='x')x.r['rp'+sd]=Math.max(+x.r['rp'+sd]||0,egN(x.r,p.sh,sd))})")
rep("function mig(p){mig2(p);migHR(p);migCK(p);migPK(p);", "function migRX(p){if(p.m19)return;Object.values(p.rows||{}).forEach(a=>{if(Array.isArray(a))a.forEach(r=>{if(!r||typeof r!='object')return;if(r.x!=null&&(r.r==null||+r.r<+r.x))r.r=+r.x||0;['R','L'].forEach(sd=>{if(r['xp'+sd]!=null&&(r['rp'+sd]==null||+r['rp'+sd]<+r['xp'+sd]))r['rp'+sd]=+r['xp'+sd]||0})})});p.m19=1}\nfunction mig(p){mig2(p);migHR(p);migCK(p);migPK(p);migRX(p);")
# app version in backups, shown on restore
rep("sav('966-backup-'+TD()+'.json',JSON.stringify(Object.assign({},dbOut(),{cfg:Object.assign({},dbOut().cfg,{ue:0,lb:nowIso()})})),'application/json')", "sav('966-backup-'+TD()+'.json',JSON.stringify(Object.assign({},dbOut(),{ver:VER,at:nowIso(),cfg:Object.assign({},dbOut().cfg,{ue:0,lb:nowIso()})})),'application/json')")
rep("blob=new Blob([JSON.stringify(Object.assign({},dbOut(),{cfg:Object.assign({},dbOut().cfg,{ue:0})}))],{type:'application/json'});const w=await nWrite(dir+'/966-auto-'", "blob=new Blob([JSON.stringify(Object.assign({},dbOut(),{ver:VER,at:nowIso(),cfg:Object.assign({},dbOut().cfg,{ue:0})}))],{type:'application/json'});const w=await nWrite(dir+'/966-auto-'")
rep("return Object.assign({},dbOut(),{cfg:Object.assign({},dbOut().cfg,{ue:0,lb:nowIso()}),_imgs:IMG,_files:files,_photos:photos})", "return Object.assign({},dbOut(),{ver:VER,at:nowIso(),cfg:Object.assign({},dbOut().cfg,{ue:0,lb:nowIso()}),_imgs:IMG,_files:files,_photos:photos})")
rep("if(!confirm('سيتم استبدال كل البيانات الحالية ('+DB.ph.length+' صيدلية) بالنسخة ('+q.ph.length+' صيدلية). متابعة؟'))return;", "if(!confirm('سيتم استبدال كل البيانات الحالية ('+DB.ph.length+' صيدلية) بالنسخة ('+q.ph.length+' صيدلية'+(q.ver?' · من إصدار '+q.ver:'')+(q.at?' · بتاريخ '+fd(q.at):'')+'). متابعة؟'))return;delete q.ver;delete q.at;")
CSS = "\n.mcl h3{margin:0 0 6px}.mcl.ok{border-color:#A8D5B5}.mcl .mcr{display:block;width:100%;text-align:start;margin:4px 0}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'تواريخ الصيدليات':'Pharmacy dates','البدء':'Start','الانتهاء':'End','إقفال الشهر':'Close the month','إقفال شهر':'Close month','اللي فاضل قبل ما تقفل الشهر. اضغط على أي سطر يوديك له.':'What is left before closing the month. Tap a line to go there.','صيدليات لسه مش مكتملة':'Pharmacies not completed','فائض ما اترحّلش للمخزن':'Surplus not moved to the warehouse','نواقص التنفيذ':'Execution shortages','نواقص الطباعة':'Print shortages','المراجعة':'Review','تمام':'OK','ما اتراجعتش':'not reviewed','مراجعة قديمة':'old review','آخر تصدير':'Last export','فيه تعديل بعده؟ صدّر تاني':'changed since? export again','لسه ما اتصدّرتش Excel / PDF':'not exported to Excel / PDF yet','مفيش فواتير للشهر ده':'No invoices this month','‹ لوحة الشهر':'‹ Month board','المستلم اتعدّل لـ':'Received set to','(المتنفذ لازم يكون مستلم)':'(executed must be received)','من إصدار':'from version','بتاريخ':'dated'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

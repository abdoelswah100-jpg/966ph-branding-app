"""v2.1: extra items (customer request) in their own management table with an editable reason, remainder closed by the
customer (billed, not a shortage), Side Acrylic Pocket under the gandola table, Acrylic boards status column,
management reports for the whole month one file per pharmacy (PDF / Excel / both) shared at once."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'XN0' not in s

# ---- A. extra item field on every type
rep("if(t.f)t.f.push({k:'nt',l:'ملاحظات (اختياري)'})",
    "if(t.f){t.f.push(Object.assign(sel('xi','بند إضافي (طلب العميل)',()=>['لا','نعم']),{hide:()=>{const p=curP();return !!(p&&(p._wh||p._rc))}}));t.f.push({k:'xn',l:'سبب البند الإضافي (بيظهر في تقرير الإدارة)',hide:d=>d.xi!='نعم'||(()=>{const p=curP();return !!(p&&(p._wh||p._rc))})()})}if(t.f)t.f.push({k:'nt',l:'ملاحظات (اختياري)'})")
# save: default reason, drop the 'no' value
rep("r[f.k]=v}\n  {const sg=y=>", "r[f.k]=v}\n  if(r.xi=='نعم'){if(!String(r.xn||'').trim())r.xn=XN0}else{delete r.xi;delete r.xn}\n  {const sg=y=>")
rep("f.k=='whm'?(rsh(y,p.sh)===2?whmOf(y):''):", "f.k=='whm'?(rsh(y,p.sh)===2?whmOf(y):''):f.k=='xi'?(y.xi=='نعم'?'نعم':''):f.k=='xn'?'':")
rep("const RCX=['q','nt','od','tw','pR','pL'];", "const RCX=['q','nt','od','tw','pR','pL','xi','xn'];")
# tags: pharmacy rows, checklist / execution rows, summary notes
rep("${isOld(p,r)?'<small class=\"rshc odt\">تصميم قديم</small>':''}${r.q!=null&&!t.nq?",
    "${isOld(p,r)?'<small class=\"rshc odt\">تصميم قديم</small>':''}${xiTag(r)}${r.cx?'<small class=\"rshc cxt\">🔖 الباقي بطلب العميل</small>':''}${r.q!=null&&!t.nq?")
rep("${isOld(x.r&&p,x.r)?'<small class=\"rshc odt\">تصميم قديم</small>':''}</td><td><b>${q}</b></td>",
    "${isOld(x.r&&p,x.r)?'<small class=\"rshc odt\">تصميم قديم</small>':''}${cxTag(x,k)}</td><td><b>${q}</b></td>")
rep("${esc(dt)}${rshT(x.r,x.s)}</td><td>—</td>", "${esc(dt)}${rshT(x.r,x.s)}${cxTag(x,k)}</td><td>—</td>")
i = s.index('function sumHtml(p){'); j = s.index('\nfunction ', i + 5); b = s[i:j]
assert b.count("esc(r.nt||'')") == 6
b = b.replace("esc(r.nt||'')", "esc(ntx(r))")
s = s[:i] + b + s[j:]

# ---- B. remainder closed by the customer: billed, not a shortage, counted done
rep("ckRows(p).forEach(x=>{const r=x.r,t=x.t,q=qn(r),v=Math.min(q,+r[k]||0),d=q-v;", "ckRows(p).forEach(x=>{if(x.r.cx)return;const r=x.r,t=x.t,q=qn(r),v=Math.min(q,+r[k]||0),d=q-v;")
rep("n+=q*f;d+=Math.min(q,+x.r[k]||0)*f;", "n+=q*f;d+=(x.r.cx?q:Math.min(q,+x.r[k]||0))*f;")
rep("n+=c;d+=Math.min(c,pkv(x.r,k,sd))", "n+=c;d+=x.r.cx?c:Math.min(c,pkv(x.r,k,sd))")

# ---- C. management rows: extra items apart, Acrylic boards by status
rep("function sizeRows(P){const m={},ord=[];function k(n,sz,mat,q,a,ty,lm){const key=n+'|'+sz+'|'+mat;if(!m[key]){m[key]={n,sz,mat,q:0,a:0,lm:0,ty:ty||n};ord.push(key)}",
    "function sizeRows(P){const m={},ord=[];function k(n,sz,mat,q,a,ty,lm,st){const key=n+'|'+sz+'|'+mat+(st!=null?'|'+st:'');if(!m[key]){m[key]={n,sz,mat,q:0,a:0,lm:0,ty:ty||n};if(st!=null)m[key].st=st;ord.push(key)}")
rep("if(t.id=='ab'){const a=ABV(r.it);k(r.it,a[0],a[1],q,0,t.n);continue}", "if(t.id=='ab'){const a=ABV(r.it);k(r.it,a[0],a[1],q,0,t.n,0,stD(r.stt)||'—');continue}")
rep("function managementReportRows(P){\n const raw=sizeRows(P)", "function managementReportRows(P0){\n const P=P0.map(p=>Object.assign({},p,{rows:xiRows(p,0)}));\n const raw=sizeRows(P)")
rep(" return raw.concat(eg);\n}", " return raw.concat(eg,xiList(P0));\n}")
# report: pockets under the gandola table, Acrylic boards table with status, extra items table
rep("all=L.map((x,i)=>({...x,_idx:i})),gandola=all.filter(x=>x.kind==='eg'),ordinary=all.filter(x=>x.kind!=='eg');const base=grpTy(ordinary)",
    "all=L.map((x,i)=>({...x,_idx:i})),gandola=all.filter(x=>x.kind==='eg'),ord0=all.filter(x=>x.kind!=='eg'&&x.kind!=='xi'),pkR=ord0.filter(x=>x.n==='Side Acrylic Pocket'),abR=ord0.filter(x=>x.st!=null),xiR=all.filter(x=>x.kind==='xi'),ordinary=ord0.filter(x=>x.n!=='Side Acrylic Pocket'&&x.st==null);const base=grpTy(ordinary)")
rep("return egTable+`<div class=\"sc\"><table id=\"rt\">", "return egTable+pkTbl(pkR,hidden)+`<div class=\"sc\"><table id=\"rt\">")
rep("${base}${more}</table></div><div class=\"fm rpadd\">", "${base}${more}</table></div>${abTbl(abR,hidden)}${xiTbl(xiR,hidden)}<div class=\"fm rpadd\">")
# review cards
rep("<span>الخامة: <b>${esc(x.mat||'—')}</b></span></div></div>`}", "<span>الخامة: <b>${esc(x.mat||'—')}</b></span>${x.st?`<span>الحالة: <b>${esc(x.st)}</b></span>`:''}${x.kind=='xi'?`<span>➕ ${esc(x.tn)} · <b>${esc(x.xn)}</b></span>`:''}</div></div>`}")
# Excel of a report element (batch)
rep("function rpXlsx(){const src=pdfClone($('#rp'))", "function rpXlsx(el){const src=pdfClone(el||$('#rp'))")
# month board / reports: batch button
rep("<button class=\"b-wa\" data-mshare=\"1\">", "<button class=\"b-wa\" data-mrb=\"1\" style=\"background:#12305C\">📤 تقارير الإدارة لكل صيدلية</button><button class=\"b-wa\" data-mshare=\"1\">")
rep("V.am=='mg'?rpWrap(", "V.am=='mg'?`<div class=\"tt np\"><button class=\"pr\" data-mrb=\"1\">📤 تقارير الإدارة لكل صيدلية لوحدها</button></div>`+rpWrap(")
rep("const TABOF={rcv:'rcv',rca:'rcv',", "const TABOF={mrb:'month',rcv:'rcv',rca:'rcv',")
rep("\n if(V.v=='mclose'){", "\n if(V.v=='mrb'){a.innerHTML=hdr('<button data-mrbx=\"1\">‹ رجوع</button>','تقارير الإدارة للشهر')+`<main>${mrbHtml()}</main>`;return}\n if(V.v=='mclose'){")
rep("x15Click(d,b)||rcvClick(d,b)||", "x15Click(d,b)||rcvClick(d,b)||v21Click(d,b)||")
rep("x15Change(x)||rcvChange(x)||", "x15Change(x)||rcvChange(x)||v21Change(x)||")
rep("const PHEDIT=['rcdel',", "const PHEDIT=['tcx','rcdel',")

JS = r"""// ---------- v2.1: extra items (customer request), remainder closed by the customer, report tables, monthly batch ----------
const XN0='العميل طلب التعديل',XIT='➕ بنود إضافية حسب طلب العميل';
const isXI=r=>!!(r&&r.xi=='نعم');
const xiTag=r=>isXI(r)?`<small class="rshc xit">➕ بند إضافي: ${esc(r.xn||XN0)}</small>`:'';
const ntx=r=>[r.nt,isXI(r)?'➕ بند إضافي: '+(r.xn||XN0):'',r.cx?'🔖 الباقي بطلب العميل':''].filter(Boolean).join(' · ');
function xiRows(p,on){const o={};Object.keys(p.rows||{}).forEach(k=>{const a=p.rows[k];o[k]=Array.isArray(a)?a.filter(r=>isXI(r)==!!on):a});return o}
function xiList(P){const o=[];P.forEach(p=>{if(!Object.values(p.rows||{}).some(a=>Array.isArray(a)&&a.some(isXI)))return;rcvIds(p);TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{if(!isXI(r))return;sizeRows([Object.assign({},p,{rows:{[t.id]:[r]}})]).forEach(x=>o.push(Object.assign(x,{kind:'xi',ty:XIT,no:p.no,pid:p.id,rid:r._i,xn:r.xn||XN0,tn:t.n})))}))});return o}
const rdelB=x=>`<td class="act"><button data-rdel="base:${x._idx}" title="حذف الصف">حذف</button></td>`;
function pkTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';return `<h3>Side Acrylic Pocket <small>(تابع للجندولة)</small></h3><div class="sc"><table><tr><th>الجهة</th><th>الخامة</th><th>العدد</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td>${x.q}</td>${rdelB(x)}</tr>`).join('')}<tr class="tot"><td colspan="2">إجمالي Side Acrylic Pocket</td><td>${v.reduce((a,x)=>a+(+x.q||0),0)} قطعة</td><td class="act"></td></tr></table></div>`}
function abTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';return `<h3>Acrylic boards</h3><div class="sc"><table><tr><th>البند</th><th>المقاس</th><th>الخامة</th><th>الحالة</th><th>العدد</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr><td>${esc(x.n)}</td><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td${x.st=='تصنيع + تركيب'?' style="background:#FAD4D4;font-weight:700"':''}>${esc(x.st)}</td><td>${x.q}</td>${rdelB(x)}</tr>`).join('')}<tr class="tot"><td colspan="4">إجمالي Acrylic boards</td><td>${v.reduce((a,x)=>a+(+x.q||0),0)} قطعة</td><td class="act"></td></tr></table></div>`}
function xiTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';const m=new Set(v.map(x=>x.pid)).size>1;return `<h3>${XIT}</h3><div class="sc"><table class="xitb"><tr>${m?'<th>الصيدلية</th>':''}<th>نوع الدعاية</th><th>المقاس</th><th>الخامة</th><th>العدد</th><th>ملاحظات</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr>${m?`<td><b>${esc(x.no)}</b></td>`:''}<td>${esc(x.n)}</td><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td>${x.n==='Wall Sticker'?x.a.toFixed(2)+' م²':x.q}</td><td contenteditable="true" data-xn="${x.pid}|${x.rid}" class="xnc">${esc(x.xn)}</td>${rdelB(x)}</tr>`).join('')}</table></div><small class="np sub">✎ اضغط على الملاحظة وعدّلها، وبتتحفظ في البند.</small>`}
document.addEventListener('focusout',e=>{const x=e.target;if(!x||!x.dataset||!x.dataset.xn)return;const[pid,rid]=x.dataset.xn.split('|'),p=DB.ph.find(q=>String(q.id)==pid);if(!p||!uEditP(p))return;let r=null;Object.values(p.rows||{}).forEach(a=>{if(Array.isArray(a)&&!r)r=a.find(y=>y&&y._i==rid)});if(!r)return;const v=x.textContent.trim()||XN0;if(v===r.xn)return;r.xn=v;p.modAt=nowIso();svq();toastT('✓ اتحفظ السبب في البند')});
// remainder closed by the customer (button in the execution list)
function cxTag(x,k){const r=x.r,c=r.cx?'<small class="rshc cxt">🔖 الباقي بطلب العميل (يتحاسب)</small>':'';const q=qn(r),pk=x.t.id=='eg'&&egSub(r,x.s),left=(!(x.t.id=='eg'&&egAO(r,x.s))&&(+r.x||0)<q)||(pk&&SDS.some(([sd])=>pkv(r,'x',sd)<egN(r,x.s,sd)));
 return xiTag(r)+c+(k=='x'&&V.v!='rcv'&&(r.cx||left)?`<button class="np tcx" data-tcx="${x.t.id}:${x.i}">${r.cx?'↺ إلغاء «بطلب العميل»':'🔖 الباقي بطلب العميل'}</button>`:'')}
// management reports of a month, one file per pharmacy
function mrbHtml(){const ms=months(),m=V.mrm||V.mo||MN(),L=DB.ph.filter(p=>p.mo==m).sort(pSort),X=V.mrx||{},f=DB.cfg.mrbf||'pdf',n=L.filter(p=>!X[p.id]).length,nf=n*(f=='both'?2:1);
 return `<div class="wcard"><h2>📤 تقارير الإدارة لكل صيدلية لوحدها</h2><p class="sub">تقرير تنفيذ للإدارة منفصل لكل صيدلية، كلهم مرة واحدة للمشاركة (واتساب).</p><label>الشهر<select id="mrbm">${(ms.includes(m)?ms:ms.concat([m])).map(x=>`<option value="${x}"${x==m?' selected':''}>${x}</option>`).join('')}</select></label>
 <div class="tt">${[['pdf','PDF'],['xlsx','Excel'],['both','الاتنين']].map(([k,t])=>`<button${f==k?' class="pr"':''} data-mrbf="${k}">${t}</button>`).join('')}</div></div>
 <div class="wcard">${L.length?L.map(p=>`<label class="mrbr"><input type="checkbox" data-mrbp="${p.id}"${X[p.id]?'':' checked'}> <b>${esc(p.no)}</b> ${esc(p.name||'')} <small>· ${esc(p.st||'')}</small></label>`).join(''):'<p class="em">مفيش صيدليات في الشهر ده.</p>'}</div>
 <div class="tt"><button class="pr big" data-mrbgo="1"${n?'':' disabled'}>${ic('share')}تجهيز ومشاركة (${nf} ملف)</button></div>`}
const mLab=m=>String(m||'').split('-').reverse().join('-');
async function shareFiles(F,msg){if(!F.length)return;
 if(CAPN()){const U=[];for(const f of F){try{const w=await nWrite(NDIR+'/'+f.name,f);U.push(w.uri)}catch(e){console.error(e)}}if(CP('Share')&&U.length){try{await CP('Share').share({title:msg,text:msg,files:U,dialogTitle:msg})}catch(e){}}toastT('✓ اتحفظ '+U.length+' ملف في Documents/'+NDIR);return}
 try{if(navigator.canShare&&navigator.canShare({files:F})){await navigator.share({files:F,title:msg,text:msg});return}}catch(e){if(e&&e.name=='AbortError')return}
 for(const f of F){dl(f.name,f,f.type);await new Promise(r=>setTimeout(r,350))}toastT('✓ اتنزّل '+F.length+' ملف. ابعتهم من واتساب')}
async function mrbGo(){const m=V.mrm||V.mo||MN(),X=V.mrx||{},L=DB.ph.filter(p=>p.mo==m&&!X[p.id]).sort(pSort),f=DB.cfg.mrbf||'pdf';if(!L.length)return;
 const t=toast('جاري تجهيز التقارير… 0 / '+L.length),F=[];
 try{for(let i=0;i<L.length;i++){const p=L[i],el=document.createElement('div');el.innerHTML=mgmtHtml(p);const nm='تقرير الإدارة - صيدلية '+p.no+' - '+mLab(m);
  if(f!='xlsx'){const b=await buildPdf(el,'تقرير تنفيذ للإدارة — '+PL(p));F.push(new File([b],nm+'.pdf',{type:'application/pdf'}))}
  if(f!='pdf'){const b=rpXlsx(el);F.push(new File([b],nm+'.xlsx',{type:b.type||'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}))}
  t.innerHTML='جاري تجهيز التقارير… '+(i+1)+' / '+L.length}}catch(e){console.error(e);t.remove();alert('تعذّر تجهيز التقارير على الجهاز ده');return}
 t.remove();window._mrbF=F;await shareFiles(F,'تقارير تنفيذ للإدارة — شهر '+mLab(m)+' — '+L.length+' صيدلية')}
function v21Click(d,b){
 if(d.tcx){const p=curP(),[tid,i]=d.tcx.split(':'),r=p&&(p.rows[tid]||[])[+i];if(!r)return 1;if(r.cx){delete r.cx}else{if(!confirm('اللي ما اتنفذش من البند ده يتحاسب في تقرير الإدارة، ومش هيظهر ناقص (طباعة ولا تنفيذ). المستلم والمتنفذ زي ما هم. تأكيد؟'))return 1;r.cx=1}p.modAt=nowIso();sv();tkRe();return 1}
 if(d.mrb){goV({v:'mrb',mrm:V.v=='all'&&V.q&&V.q.mo?V.q.mo:(V.mo||MN()),bk:V.v,bam:V.am,op:{},dr:{},q:V.q});return 1}
 if(d.mrbx){const k=V.bk||'month';goV(k=='all'?{v:'all',am:V.bam||'mg',op:{},dr:{},q:V.q}:{v:k,op:{},dr:{},q:V.q});return 1}
 if(d.mrbf){DB.cfg.mrbf=d.mrbf;svq();render();return 1}
 if(d.mrbgo){mrbGo();return 1}
 return 0}
function v21Change(x){
 if(x.id=='mrbm'){V.mrm=x.value;V.mrx={};render();return 1}
 if(x.dataset&&x.dataset.mrbp){V.mrx=V.mrx||{};if(x.checked)delete V.mrx[x.dataset.mrbp];else V.mrx[x.dataset.mrbp]=1;render();return 1}
 return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
CSS = "\n.rshc.xit{background:#E6F4D2;color:#2E5E0E}.rshc.cxt{background:#FFEFD6;color:#8A5300}.tcx{display:block;margin-top:4px;font-size:12px;padding:3px 8px}.xnc{background:rgba(168,216,110,.18);min-width:120px}.mrbr{display:flex;gap:8px;align-items:center;padding:8px 2px;border-bottom:1px solid var(--ln);font-size:14px;color:var(--tx)}.mrbr input{width:20px;height:20px}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
# version
rep("VER='v2.0'", "VER='v2.1'")
rep(" changelog:[{version:'v2.0',", " changelog:[{version:'v2.1',date:'2026-10-31',changes:['Extra item (customer request) on every type: own table in the management report with the reason (default العميل طلب التعديل, editable there, shown in notes)','🔖 Remainder by the customer: billed, not a print / execution shortage, counted done; received and executed unchanged; surplus to the warehouse as before','Management report: Side Acrylic Pocket right under the End gandola table; Acrylic boards table with status (تركيب فقط / تصنيع + تركيب in light red)','📤 Management reports of a month, one file per pharmacy (PDF / Excel / both), shared at once']},{version:'v2.0',")
EN = {'بند إضافي (طلب العميل)':'Extra item (customer request)','سبب البند الإضافي (بيظهر في تقرير الإدارة)':'Reason for the extra item (shown in the management report)','العميل طلب التعديل':'Requested by the customer','➕ بنود إضافية حسب طلب العميل':'➕ Extra items requested by the customer','🔖 الباقي بطلب العميل':'🔖 Rest by customer request','↺ إلغاء «بطلب العميل»':'↺ Undo «customer request»','🔖 الباقي بطلب العميل (يتحاسب)':'🔖 Rest by customer request (billed)','(تابع للجندولة)':'(part of the gandola)','الحالة':'Status','تقارير الإدارة للشهر':'Management reports of the month','📤 تقارير الإدارة لكل صيدلية':'📤 Management report per pharmacy','📤 تقارير الإدارة لكل صيدلية لوحدها':'📤 Management report for each pharmacy','الاتنين':'Both','✎ اضغط على الملاحظة وعدّلها، وبتتحفظ في البند.':'✎ Tap the note to edit it; it is saved on the item.','✓ اتحفظ السبب في البند':'✓ Reason saved on the item'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

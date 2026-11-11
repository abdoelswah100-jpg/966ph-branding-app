"""v3.7: warehouse import from a file (adds to the stock, preview first); Floor Header «رولاند» stock (separate, asked first
when pulling, shortages marked «اطبع على رولاند», stays until closed); End gandola parts each on its own: header / side /
side acrylic counts per row (automatic 1 / 2 / 0 per gandola, editable) everywhere (summary, reports, shortages,
checklists, warehouse); maintenance «End gandola - Side Acrylic»."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'egFh(' not in s
JS, CSS, EN = [], [], {}

# =====================================================================
# 1. End gandola parts
# =====================================================================
rep("num('q','عدد الجندولات'),...SDS.map(([sd,n])=>",
    "num('q','عدد الجندولات'),Object.assign(num('eh','عدد الهيدر'),{opt:1,z0:1,hint:'فاضي = تلقائي (هيدر لكل جندولة). اكتب 0 لو مش محتاج هيدر.',hide:(d,s)=>egpOf(d,s)===EGPO[2]}),Object.assign(num('es','عدد السايد'),{opt:1,z0:1,hint:'فاضي = تلقائي (2 سايد لكل جندولة). اكتب 0 لو مش محتاج سايد.',hide:(d,s)=>egpOf(d,s)===EGPO[2]}),Object.assign(num('ea','أكريليك السايد (عدد القطع)'),{opt:1,z0:1,hint:'اختياري (نادر). المقاس نفس مقاس ستيكر السايد.',hide:(d,s)=>rsh(d,s)===2}),...SDS.map(([sd,n])=>")
rep("  return `${r.nm} · Header ${h} (${hm}) ×${q} + Side ${sd} (${sm}) ×${PARTS.eg[1][1]*q}${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket ${pkZ(r,q)}`:''}`}},",
    "  const H=egRd(egFh(r)*q),S=egRd(egFs(r)*q),A=egRd(egFa(r)*q),pt=[H?`Header ${h} (${hm}) ×${H}`:'',S?`Side ${sd} (${sm}) ×${S}`:'',A?`Side Acrylic ${sd} (أكريليك) ×${A}`:''].filter(Boolean).join(' + ');\n  return `${r.nm} · ${pt||'—'}${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket ${pkZ(r,q)}`:''}`}},")
# totals line
rep("if(t.id=='eg'&&s!=null){const hq=rs.filter(r=>egHS(r,s)).reduce((a,r)=>a+(+r.q||0),0),pr=rs.reduce((a,r)=>a+egN(r,s,'R'),0),pl=rs.reduce((a,r)=>a+egN(r,s,'L'),0);return PARTS.eg.map(([n,f])=>n+' '+f*hq).join(' · ')+(pr+pl?",
    "if(t.id=='eg'&&s!=null){const E=rs.filter(r=>egHS(r,s)),H=egRd(E.reduce((a,r)=>a+egFh(r)*(+r.q||0),0)),S=egRd(E.reduce((a,r)=>a+egFs(r)*(+r.q||0),0)),A=egRd(rs.reduce((a,r)=>a+egFa(r)*(+r.q||0),0)),pr=rs.reduce((a,r)=>a+egN(r,s,'R'),0),pl=rs.reduce((a,r)=>a+egN(r,s,'L'),0);return 'Header '+H+' · Side '+S+(A?' · Side Acrylic '+A:'')+(pr+pl?")
# all-pharmacies aggregate
rep("k(t.n,sc,q,t.m?t.m(r):0);if(t.id=='eg')k('End gandola (Side)',sc,PARTS.eg[1][1]*q,0)}}",
    "if(t.id=='eg'){k(t.n,sc,egRd(egFh(r)*q),0);k('End gandola (Side)',sc,egRd(egFs(r)*q),0);if(egFa(r))k('End gandola (Side Acrylic)',sc,egRd(egFa(r)*q),0)}else k(t.n,sc,q,t.m?t.m(r):0)}}")
# sizes report
rep("if(t.id=='eg'){const x=EGR.exec(z);if(x){k('End gandola - Header',x[1],x[2],q);k('End gandola - Side',x[3],x[4],PARTS.eg[1][1]*q)}",
    "if(t.id=='eg'){const x=egAO(r,p.sh)?null:egSz(r,p.sh);if(x){if(egFh(r))k('End gandola - Header',x.h,x.hm,egRd(egFh(r)*q));if(egFs(r))k('End gandola - Side',x.sd,x.sm,egRd(egFs(r)*q));if(egFa(r))k('End gandola - Side Acrylic',x.sd,'أكريليك',egRd(egFa(r)*q))}")
# management report
rep("x.q+=q;x.header+=PARTS.eg[0][1]*q;x.side+=PARTS.eg[1][1]*q;}", "x.q+=q;x.header+=egRd(egFh(r)*q);x.side+=egRd(egFs(r)*q);}")
# progress
rep("f=x.t.id=='eg'&&egAO(x.r,x.s)?0:x.t.id=='md'?", "f=x.t.id=='eg'&&egAO(x.r,x.s)?0:x.t.id=='eg'?egFh(x.r)+egFs(x.r)+egFa(x.r):x.t.id=='md'?")
# shortages
rep("const m=EGR.exec(t.z(r,p.sh)),f=PARTS.eg[1][1];if(d>0){o.push({...b,nm:r.nm,pt:'Header',sz:m?m[1]:'—',mat:m?m[2]:'—',q,v,d});o.push({...b,nm:r.nm,pt:'Side',sz:m?m[3]:'—',mat:m?m[4]:'—',q:f*q,v:f*v,d:f*d})}",
    "const m=egSz(r,p.sh),fh=egFh(r),f=egFs(r),fa=egFa(r);if(d>0){if(fh)o.push({...b,nm:r.nm,pt:'Header',sz:m.h,mat:m.hm,q:egRd(fh*q),v:egRd(fh*v),d:egRd(fh*q)-egRd(fh*v)});if(f)o.push({...b,nm:r.nm,pt:'Side',sz:m.sd,mat:m.sm,q:egRd(f*q),v:egRd(f*v),d:egRd(f*q)-egRd(f*v)});if(fa)o.push({...b,nm:r.nm,pt:'Side Acrylic',sz:m.sd,mat:'أكريليك',q:egRd(fa*q),v:egRd(fa*v),d:egRd(fa*q)-egRd(fa*v)})}")
# warehouse parts
rep(" if(t.id=='eg'){const m=EGR.exec(z);if(m){L.push({ty:'End gandola - Header',nm,sec,size:m[1],mat:m[2],f:PARTS.eg[0][1]});L.push({ty:'End gandola - Side',nm,sec,size:m[3],mat:m[4],f:PARTS.eg[1][1]})}",
    " if(t.id=='eg'){const m=egAO(r,s)?null:egSz(r,s);if(m){if(egFh(r))L.push({ty:'End gandola - Header',nm,sec,size:m.h,mat:m.hm,f:egFh(r)});if(egFs(r))L.push({ty:'End gandola - Side',nm,sec,size:m.sd,mat:m.sm,f:egFs(r)});if(egFa(r))L.push({ty:'End gandola - Side Acrylic',nm,sec,size:m.sd,mat:'أكريليك',f:egFa(r)})}")
# old stock offer uses the row's sides / acrylic
rep("if(need>0&&t.id=='eg'&&sh<=1){const n=PARTS.eg[1][1]*need;W.filter(x=>(x.ty==OLDT.egs&&(x.nm==r.nm||(x.sec&&x.sec==egSec(r.nm))))||x.ty==OLDT.beg).forEach(x=>add(x,n,'o',x.ty==OLDT.egs?'سايد أكريليك تصميم قديم':'أكريليك فاضي للسايد '+OGS))}",
    "if(need>0&&t.id=='eg'&&sh<=1){const ns=egRd(egFs(r)*need),na=egRd(egFa(r)*need);W.filter(x=>(x.ty==OLDT.egs&&(x.nm==r.nm||(x.sec&&x.sec==egSec(r.nm))))||x.ty==OLDT.beg).forEach(x=>{const n=x.ty==OLDT.egs?ns:(na||ns);if(n>0)add(x,n,'o',x.ty==OLDT.egs?'سايد أكريليك تصميم قديم':'أكريليك فاضي للسايد '+OGS)})}")
# maintenance types
rep("concat(['End gandola - Header','End gandola - Side','Side Acrylic','أخرى'])", "concat(['End gandola - Header','End gandola - Side','End gandola - Side Acrylic','Side Acrylic','أخرى'])")
JS.append(r"""// ---------- v3.7: End gandola parts (per gandola factors; empty field = automatic 1 header / 2 sides / 0 acrylic) ----------
const egSet=v=>v!==undefined&&v!==null&&v!=='';
const egRd=x=>Math.round((+x||0)*100)/100;
function egFh(r){if(!r||!egSet(r.eh))return 1;const q=qn(r);return q>0?Math.max(0,+r.eh||0)/q:0}
function egFs(r){if(!r||!egSet(r.es))return PARTS.eg[1][1];const q=qn(r);return q>0?Math.max(0,+r.es||0)/q:0}
function egFa(r){if(!r||!egSet(r.ea)||+r.ea<=0)return 0;const q=qn(r);return q>0?(+r.ea)/q:0}
function egSz(r,s){const b=r.sz=='كبير',c=x=>String(x).replace(/\s+/g,'');return {h:c(SZ(b?'eg.hl':'eg.hs')[s]),sd:c(SZ(b?'eg.sl':'eg.ss')[s]),hm:SZ('mt.egh')[s],sm:SZ('mt.egs')[s]}}
""")
EN.update({'عدد الهيدر':'Number of headers','عدد السايد':'Number of sides','أكريليك السايد (عدد القطع)':'Side acrylic (pieces)'})

# =====================================================================
# 2. Floor Header «رولاند»
# =====================================================================
rep("<label>نوع الرفوف<select id=\"whash\">${SH.map((x,i)=>`<option value=\"${i}\"${p.sh==i?' selected':''}>${x}</option>`).join('')}</select></label></div>",
    "<label>نوع الرفوف<select id=\"whash\">${SH.map((x,i)=>`<option value=\"${i}\"${p.sh==i?' selected':''}>${x}</option>`).join('')}</select></label>${rolOn()&&p.sh!=2?`<label class=\"chk rolt${V.whRol?' on':''}\"><input type=\"checkbox\" id=\"whrol\"${V.whRol?' checked':''}> 🖨 Floor Header رولاند (مات فيلم طباعة رولاند — ألوان مختلفة، بيتحفظ لوحده)</label>`:''}</div>")
rep("function whaSave(){const p=WHP();let n=0;TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{const q=qn(r);whParts(t,r,p.sh).forEach(y=>{whAdd({sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:y.mat,size:y.size},wq(q*y.f),'in','manual','إضافة للمخزن');n++})}));",
    "function whaSave(){const p=WHP(),rl=V.whRol&&rolOn();let n=0;TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{const q=qn(r);whParts(t,r,p.sh).forEach(y=>{const R=rl&&t.id=='fh'&&y.sh!=2;const x=whAdd({sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:R?'مات فيلم'+ROLM:y.mat,size:y.size},wq(q*y.f),'in','manual',R?'إضافة للمخزن · رولاند':'إضافة للمخزن');if(R)x.rol=1;n++})}));V.whRol=false;")
rep("const L=W0.filter(x=>(!F.old||x.old)&&", "const L=W0.filter(x=>(!F.old||x.old)&&(!F.rol||x.rol)&&")
rep("${W.some(x=>x.old)?`<button class=\"${F.old?'pr':''} whold\" data-whold=\"1\">", "${W.some(x=>x.rol)?`<button class=\"${F.rol?'pr':''} whold\" data-whrolf=\"1\">🖨 رولاند <small>${W.filter(x=>x.rol).length}</small></button>`:''}${W.some(x=>x.old)?`<button class=\"${F.old?'pr':''} whold\" data-whold=\"1\">")
rep("<div class=\"whi\"><b>${esc(x.ty)}${x.old&&", "<div class=\"whi\"><b>${esc(x.ty)}${x.rol?' <small class=\"rshc rolc\">🖨 رولاند</small>':''}${x.old&&")
rep("${whLow()?`<div class=\"alr\"><small>⚠ ${whLow()} صنف رصيده وصل للحد الأدنى أو أقل.</small></div>`:''}${whOutHtml()}",
    "${whLow()?`<div class=\"alr\"><small>⚠ ${whLow()} صنف رصيده وصل للحد الأدنى أو أقل.</small></div>`:''}${whOutHtml()}${rolBar()}")
# offered first when pulling, and the automatic offer asks with the Roland choice first
rep("function whFromOpts(p,t,r){if(!p||p._wh||p._rc||!WU().length)return [];const need=Math.max(0,qn(r)-(+r.r||0)),o=[];",
    "function whFromOpts(p,t,r){if(!p||p._wh||p._rc||!WU().length)return [];const need=Math.max(0,qn(r)-(+r.r||0)),o=rolOpts(p,t,r);")
rep("function whPullOffer(p,t,r){if(!p||p._wh||p._rc||!WU().length)return;const L=whRowPlan(t,r,p.sh);",
    "function whPullOffer(p,t,r){if(!p||p._wh||p._rc||!WU().length)return;if(rolOpts(p,t,r).length){const i=(p.rows[t.id]||[]).indexOf(r);if(i>=0)return whFrom(p,t,r,i)}const L=whRowPlan(t,r,p.sh);")
rep(" const tt=toast(`<span>📦 من المخزن للبند ده (${esc(t.n)}):</span>${O.map((o,j)=>`<button class=\"pr\" data-whf2=\"${j}\">اسحب ${esc(o.txt)}</button>`).join('')}<button data-tclose=\"1\">لا</button>`);",
    " const tt=toast(`<span>📦 من المخزن للبند ده (${esc(t.n)}):${O.some(o=>o.rol)?'<br><b>🖨 فيه Floor Header رولاند بنفس المقاس. تسحب منه؟ (لو سحبت منه، نواقص الصيدلية دي هتتعلّم «اطبع على رولاند»)</b>':''}</span>${O.map((o,j)=>`<button class=\"pr${o.rol?' rolb':''}\" data-whf2=\"${j}\">اسحب ${esc(o.txt)}</button>`).join('')}<button data-tclose=\"1\">لا</button>`);")
rep("function whFrom2(tt,j){const o=tt._wf,p=DB.ph.find(x=>x.id==o.pid);if(!p)return;const t=T.find(x=>x.id==o.tid),r=(p.rows[o.tid]||[])[o.i],c=o.O[j];if(!t||!r||!c)return;",
    "function whFrom2(tt,j){const o=tt._wf,p=DB.ph.find(x=>x.id==o.pid);if(!p)return;const t=T.find(x=>x.id==o.tid),r=(p.rows[o.tid]||[])[o.i],c=o.O[j];if(!t||!r||!c)return;if(c.rol){p.rol=1;r.rol=1;p.modAt=nowIso()}")
rep("x.old?'سحب تصميم قديم لبند في الصيدلية':'سحب لبند في الصيدلية (مقاس تاني)'", "x.old?'سحب تصميم قديم لبند في الصيدلية':x.rol?'سحب رولاند لبند في الصيدلية':'سحب لبند في الصيدلية (مقاس تاني)'")
# shortages of a pharmacy that took Roland: Floor Header printed on Roland
rep("  o.push({...b,nm,pt:'',sz,mat,sd:r.sd||'',stt:t.id=='ab'?stD(r.stt):'',q,v,d})});return o}",
    "  o.push({...b,nm,pt:'',sz,mat:t.id=='fh'&&p.rol?mat+' · 🖨 اطبع على رولاند':mat,sd:r.sd||'',stt:t.id=='ab'?stD(r.stt):'',q,v,d})});return o}")
JS.append(r"""// ---------- v3.7: Floor Header «رولاند» ----------
const ROLM=' · رولاند';
const rolOn=()=>!(DB.cfg&&DB.cfg.rolOff);
function rolOpts(p,t,r){if(!p||p._wh||p._rc||t.id!='fh'||!rolOn())return [];const need=Math.max(0,qn(r)-(+r.r||0));if(!need)return [];const sz=v=>String(v||'').replace(/\s+/g,''),P=whParts(t,r,p.sh)[0];if(!P)return [];
 return WU().filter(x=>x.rol&&+x.qty>=1&&x.ty==P.ty&&x.nm==P.nm&&x.sec==P.sec&&sz(x.size)==sz(P.size)).sort((a,b)=>(a.sh==P.sh?0:1)-(b.sh==P.sh?0:1)).map(x=>{const n=Math.min(need,Math.floor(+x.qty));return {k:'a',id:x.id,n,rol:1,txt:`🖨 ${n} رولاند (مات فيلم) · ${x.size}${x.sh!=P.sh?' · من مخزن '+SH[x.sh]:''} (في المخزن ${wq(x.qty)})`}}).filter(o=>o.n>0)}
function rolBar(){const L=WU().filter(x=>x.rol),n=wq(L.reduce((a,x)=>a+(+x.qty||0),0));if(!rolOn())return '';return `<div class="rolbar"><span>🖨 Floor Header رولاند: <b>${n}</b> قطعة في ${L.length} صنف${L.length?'':' (ضيفه من «إضافة للمخزن» وعلّم «رولاند»)'}</span><button class="np" data-rolx="1">قفل رولاند</button></div>`}
function v37Click(d,b){
 if(d.whrolf){V.wf=V.wf||{};V.wf.rol=!V.wf.rol;if(V.wf.rol)V.wf.sh='';render();return 1}
 if(d.rolx){const n=wq(WU().filter(x=>x.rol).reduce((a,x)=>a+(+x.qty||0),0));if(confirm('قفل خيار رولاند؟'+(n?'\nلسه فيه '+n+' قطعة رولاند في المخزن (هتفضل في القائمة، بس مش هتتعرض للسحب).':'')+'\nتقدر تفتحه تاني من «إضافة للمخزن».')){DB.cfg.rolOff=1;sv();render()}return 1}
 if(d.rolon){delete DB.cfg.rolOff;sv();render();return 1}
 if(d.whimp){const i=$('#whimpin');if(i)i.click();return 1}
 if(d.whimgo){whImpGo();return 1}
 return 0}
function v37Change(x){
 if(x.id=='whrol'){V.whRol=x.checked;render();return 1}
 if(x.id=='whimpin'){const f=x.files&&x.files[0];x.value='';if(f)f.text().then(t=>{let q;try{q=JSON.parse(t)}catch(e){return alert('ملف غير صالح')}whImpOpen(q,f.name)});return 1}
 return 0}
""")
rep("v33Click(d,b)||v34Click(d,b)||", "v33Click(d,b)||v34Click(d,b)||v37Click(d,b)||")
rep("v33Change(x)||v34Change(x)||", "v33Change(x)||v34Change(x)||v37Change(x)||")
rep("<button class=\"lnk\" data-whoa=\"1\">🕰 إضافة مخزون قديم (تصميم قديم / أكريليك فاضي) ›</button>`}",
    "<button class=\"lnk\" data-whoa=\"1\">🕰 إضافة مخزون قديم (تصميم قديم / أكريليك فاضي) ›</button><button class=\"lnk\" data-whimp=\"1\">📥 استيراد أصناف مخزن من ملف ›</button><input type=\"file\" id=\"whimpin\" accept=\".json,application/json\" hidden>${rolOn()?'':'<button class=\"lnk\" data-rolon=\"1\">🖨 فتح خيار رولاند تاني ›</button>'}`}")
CSS.append(".rolt{background:#EEF2FF;border:1px dashed #6366F1;border-radius:10px;padding:8px}.rolt.on{background:#E0E7FF}.rolc{background:#E0E7FF!important;color:#3730A3!important}.rolbar{display:flex;align-items:center;justify-content:space-between;gap:8px;background:#EEF2FF;border:1px solid #C7D2FE;color:#3730A3;border-radius:10px;padding:8px 10px;margin:8px 0;font-size:13px}.toast .rolb{background:#4F46E5!important;border-color:#4F46E5!important}")
EN.update({'قفل رولاند':'Close Roland','رولاند':'Roland','اطبع على رولاند':'print on Roland'})

# =====================================================================
# 3. warehouse import from a file: {"kind":"966-warehouse","items":[{sh,ty,nm,sec,mat,size,qty,old,real,solo,rol,unit}]}
# =====================================================================
rep("const q=JSON.parse(rd.result);if(q&&q.kind==SKIND){doSync(q);return}", "const q=JSON.parse(rd.result);if(q&&q.kind==SKIND){doSync(q);return}if(q&&q.kind=='966-warehouse'){whImpOpen(q,f.name);return}")
JS.append(r"""// ---------- v3.7: warehouse import ----------
let WIMP=null;
function whImpNorm(z){const shi=typeof z.sh=='number'?z.sh:SH.indexOf(String(z.sh||''));return {sh:shi>=0?shi:-1,ty:String(z.ty||'').trim(),nm:String(z.nm||'').trim(),sec:String(z.sec||'').trim(),mat:String(z.mat||'').trim(),size:String(z.size||'').trim().replace(/\s*[x×*]\s*/i,'×'),qty:wq(+z.qty||0),old:z.old?1:0,real:z.real?String(z.real).trim():'',solo:z.solo?1:0,rol:z.rol?1:0,unit:z.unit||''}}
function whImpOpen(q,fn){const L=(q.items||[]).map(whImpNorm).filter(x=>x.ty&&x.qty>0);if(!L.length)return alert('الملف مفيهوش أصناف صالحة');WIMP={L,fn:fn||'ملف'};cShClose();const el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>📥 استيراد ${L.length} صنف للمخزن</b><small>${esc(WIMP.fn)}${q.note?' · '+esc(q.note):''}. الأصناف بتتضاف على الرصيد الحالي، ومفيش حاجة بتتمسح.</small>
 <div class="cnpl">${L.map(x=>{const e=WU().find(y=>whKey(y)==whKey(x));return `<div class="cnpi"><b>+${wq(x.qty)}</b><span>${esc(x.ty)}${x.nm?' · '+esc(x.nm):''}${x.sec?' · '+esc(x.sec):''}<small>${esc(x.size||'—')}${x.real?' (فعلي '+esc(x.real)+')':''} · ${esc(x.mat||'—')} · ${x.sh>=0?SH[x.sh]:'—'}${x.old?' · 🕰 تصميم قديم':''}${x.rol?' · 🖨 رولاند':''}${e?' · الرصيد دلوقتي '+wq(e.qty):' · صنف جديد'}</small></span></div>`}).join('')}</div>
 <div class="cshr"><button class="pr" data-whimgo="1">${ic('check')}ضيفهم للمخزن</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function whImpGo(){if(!WIMP)return;let n=0;WIMP.L.forEach(z=>{const o={sh:z.sh,ty:z.ty,nm:z.nm,sec:z.sec,mat:z.mat,size:z.size};if(z.old)o.old=1;const x=whAdd(o,z.qty,'in','import','استيراد من ملف · '+WIMP.fn);if(z.old)x.old=1;if(z.real)x.real=z.real;if(z.solo)x.solo=1;if(z.rol)x.rol=1;if(z.unit)x.unit=z.unit;n++});WIMP=null;cShClose();sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتضاف '+n+' صنف للمخزن')}
""")
EN.update({'📥 استيراد أصناف مخزن من ملف ›':'📥 Import warehouse items from a file ›','ضيفهم للمخزن':'Add them to the warehouse'})

# =====================================================================
# write
# =====================================================================
rep("// ---------- v1.5 extras ----------", '\n'.join(JS) + "// ---------- v1.5 extras ----------")
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}\n" + ''.join(CSS) + "\n")
rep("VER='v3.6'", "VER='v3.7'")
rep(" changelog:[{version:'v3.6',", " changelog:[{version:'v3.7',date:'2026-11-10',changes:['Warehouse import from a file (kind 966-warehouse): preview, adds to the stock, nothing deleted','Floor Header «رولاند» stock (all shelf types except Old Turkish): separate items, chip, offered first and asked when pulling, the pharmacy shortages of Floor Header marked «اطبع على رولاند», stays until closed','End gandola: header / side / side acrylic counts per row (empty = automatic 1 / 2 / 0 per gandola, 0 = none), used in the summary, reports, shortages, checklists and warehouse; so each part can be added alone in pharmacies and the warehouse; maintenance type «End gandola - Side Acrylic»']},{version:'v3.6',")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

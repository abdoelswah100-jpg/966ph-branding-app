"""v1.6 part 2: Old Turkish gondola acrylic pocket counted on its own: number to make (pq), received / executed (rp / xp),
shortages, progress, warehouse (surplus and pull per part group)."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:140]}')
    s = s.replace(a, b)
assert 'egPq' not in s
# helpers
rep("egPK=(r,s)=>rsh(r,s)===2&&egpOf(r,s)!==EGPO[1];",
    "egPK=(r,s)=>rsh(r,s)===2&&egpOf(r,s)!==EGPO[1];\n// pocket pairs to make; acrylic-only rows: the row count itself; full rows: pq (empty = number of gondolas)\nconst egAO=(r,s)=>egpOf(r,s)===EGPO[2],egSub=(r,s)=>egPK(r,s)&&!egAO(r,s),egPq=(r,s)=>!egPK(r,s)?0:egAO(r,s)?qn(r):(r.pq!==undefined&&r.pq!==null&&r.pq!==''?Math.max(0,Math.round(+r.pq||0)):qn(r)),pkv=(r,k)=>+r[k+'p']||0;")
# field: number of pockets (only full rows on Old Turkish)
rep("Object.assign(sel('egp','المطلوب',()=>EGPO),{hide:(d,s)=>rsh(d,s)!==2}),num('q','عدد الجندولات')],",
    "Object.assign(sel('egp','المطلوب',()=>EGPO),{hide:(d,s)=>rsh(d,s)!==2}),num('q','عدد الجندولات'),Object.assign(num('pq','عدد جيوب الأكريليك المطلوب تصنيعها (فاضي = نفس عدد الجندولات)'),{opt:1,hide:(d,s)=>rsh(d,s)!==2||(EGPO.includes(d.egp)?d.egp:EGPO[0])!==EGPO[0]})],")
rep("${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket (1L + 1R)`:''}`}},", "${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket (1L + 1R)${r.pq!=null&&r.pq!==''&&+r.pq!==+q?' ×'+(+r.pq):''}`:''}`}},")
# add / edit: hidden and optional fields; keep the pocket counters on edit
rep("for(const f of t.f){let v=dd[f.k];if(f.n){", "for(const f of t.f){let v=dd[f.k];if(f.hide&&f.hide(dd,p.sh))continue;if(f.opt&&(v===''||v==null))continue;if(f.n){")
rep("['r','x'].forEach(k=>{if(o0[k]!=null)r[k]=Math.min(+o0[k]||0,qq)})", "['r','x'].forEach(k=>{if(o0[k]!=null)r[k]=Math.min(+o0[k]||0,qq);if(o0[k+'p']!=null)r[k+'p']=Math.min(+o0[k+'p']||0,egPq(r,p.sh))});['wf','wfp'].forEach(k=>{if(o0[k]!=null)r[k]=o0[k]})")
rep("const FPX=['ck','nt','r','x','wf'];", "const FPX=['ck','nt','r','x','wf','rp','xp','wfp'];")
# migration: old receipts keep the pocket with the header / side
rep("function mig(p){mig2(p);migHR(p);migCK(p);", "function migPK(p){if(p.m16)return;((p.rows||{}).eg||[]).forEach(r=>{if(!egSub(r,p.sh))return;['r','x'].forEach(k=>{if(r[k]!=null&&r[k+'p']==null)r[k+'p']=Math.min(egPq(r,p.sh),+r[k]||0)})});p.m16=1}\nfunction mig(p){mig2(p);migHR(p);migCK(p);migPK(p);")
# progress
rep("ckRows(p).forEach(x=>{const q=qn(x.r),f=pcs(x.t);n+=q*f;d+=Math.min(q,+x.r[k]||0)*f})",
    "ckRows(p).forEach(x=>{const q=qn(x.r),f=x.t.id=='eg'&&egAO(x.r,x.s)?2:pcs(x.t);n+=q*f;d+=Math.min(q,+x.r[k]||0)*f;if(x.t.id=='eg'&&egSub(x.r,x.s)){const pq=egPq(x.r,x.s);n+=2*pq;d+=2*Math.min(pq,pkv(x.r,k))}})")
# checklist rows: a pocket line under each full gondola
rep("""<button class="np tkf" data-tf="${id}">✓</button></div></td></tr>`}).join('')+`<tr class="tot"><td colspan="2">إجمالي ${esc(g.t.n)}</td>""",
    """<button class="np tkf" data-tf="${id}">✓</button></div></td></tr>`+tkPk(x,k)}).join('')+`<tr class="tot"><td colspan="2">إجمالي ${esc(g.t.n)}</td>""")
rep("function tkSet(p,k,tid,i,v){const r=p.rows[tid]&&p.rows[tid][+i];if(!r)return;const q=qn(r);v=Math.max(0,Math.round(+v||0));r[k]=v;if(k=='x'&&v>(+r.r||0))toastT('⚠ المتنفذ ('+v+') أكتر من المستلم من الطباعة ('+(+r.r||0)+')');",
    "function tkPk(x,k){if(x.t.id!='eg'||!egSub(x.r,x.s))return '';const q=egPq(x.r,x.s);if(!q)return '';const v=pkv(x.r,k),st=v>=q?'ok':v>0?'pt':'no',id=k+'p:'+x.t.id+':'+x.i;\n return `<tr class=\"tk-${st} tkp\"><td>↳</td><td>Side Acrylic Pocket (1L + 1R) · أكريليك</td><td><b>${q}</b></td><td><div class=\"tkv\"><button class=\"np\" data-tk=\"${id}:-1\" aria-label=\"ناقص\">−</button><input type=\"number\" inputmode=\"numeric\" min=\"0\" data-tv=\"${id}\" value=\"${v}\"><button class=\"np\" data-tk=\"${id}:1\" aria-label=\"زائد\">+</button><button class=\"np tkf\" data-tf=\"${id}\">✓</button></div></td></tr>`}\nfunction tkSet(p,k,tid,i,v){const r=p.rows[tid]&&p.rows[tid][+i];if(!r)return;const pk=k.length==2,q=pk?egPq(r,p.sh):qn(r);v=Math.max(0,Math.round(+v||0));r[k]=v;{const rv=pk?pkv(r,'r'):(+r.r||0);if(k[0]=='x'&&v>rv)toastT('⚠ المتنفذ ('+v+') أكتر من المستلم من الطباعة ('+rv+')')}")
# clicks: +/−, ✓ per row / group / all, clear
rep("if(d.tk){const[k,tid,i,dv]=d.tk.split(':'),r=p.rows[tid][+i];tkSet(p,k,tid,i,(+r[k]||0)+(+dv))}else if(d.tf){const[k,tid,i]=d.tf.split(':'),r=p.rows[tid][+i],q=qn(r);tkSet(p,k,tid,i,(+r[k]||0)>=q?0:q)}else if(d.tkt){const[k,tid]=d.tkt.split(':');(p.rows[tid]||[]).forEach((r,i)=>{if(qn(r)>0)r[k]=qn(r)})}else if(d.tkall){ckRows(p).forEach(x=>{x.r[d.tkall]=qn(x.r)})}else{if(!confirm('تصفير كل الأعداد في القايمة دي؟'))return;ckRows(p).forEach(x=>{x.r[d.tkclr]=0})}",
    "if(d.tk){const[k,tid,i,dv]=d.tk.split(':'),r=p.rows[tid][+i];tkSet(p,k,tid,i,(+r[k]||0)+(+dv))}else if(d.tf){const[k,tid,i]=d.tf.split(':'),r=p.rows[tid][+i],q=k.length==2?egPq(r,p.sh):qn(r);tkSet(p,k,tid,i,(+r[k]||0)>=q?0:q)}else if(d.tkt){const[k,tid]=d.tkt.split(':');(p.rows[tid]||[]).forEach((r,i)=>{if(qn(r)>0)r[k]=qn(r);if(tid=='eg'&&egSub(r,p.sh))r[k+'p']=egPq(r,p.sh)})}else if(d.tkall){ckRows(p).forEach(x=>{x.r[d.tkall]=qn(x.r);if(x.t.id=='eg'&&egSub(x.r,p.sh))x.r[d.tkall+'p']=egPq(x.r,p.sh)})}else{if(!confirm('تصفير كل الأعداد في القايمة دي؟'))return;ckRows(p).forEach(x=>{x.r[d.tkclr]=0;if(x.r[d.tkclr+'p']!=null)x.r[d.tkclr+'p']=0})}")
# shortages
rep("function nqLines(p,k){const o=[];ckRows(p).forEach(x=>{const r=x.r,t=x.t,q=qn(r),v=Math.min(q,+r[k]||0),d=q-v;if(d<=0)return;const z=t.z(r,p.sh),sc=t.id=='ab'?'':scOf(r),b={p,t,r,sec:sc};\n  if(t.id=='eg'){const m=EGR.exec(z);o.push({...b,nm:r.nm,pt:'Header',sz:m?m[1]:'—',mat:m?m[2]:'—',q,v,d});const f=PARTS.eg[1][1];o.push({...b,nm:r.nm,pt:'Side',sz:m?m[3]:'—',mat:m?m[4]:'—',q:f*q,v:f*v,d:f*d});return}",
    "function nqLines(p,k){const o=[];ckRows(p).forEach(x=>{const r=x.r,t=x.t,q=qn(r),v=Math.min(q,+r[k]||0),d=q-v;\n  if(t.id=='eg'){const b={p,t,r,sec:scOf(r)},PK={...b,nm:r.nm,pt:'Side Acrylic Pocket',sz:'1L + 1R',mat:'أكريليك'};if(egAO(r,p.sh)){if(d>0)o.push({...PK,q,v,d});return}const m=EGR.exec(t.z(r,p.sh)),f=PARTS.eg[1][1];if(d>0){o.push({...b,nm:r.nm,pt:'Header',sz:m?m[1]:'—',mat:m?m[2]:'—',q,v,d});o.push({...b,nm:r.nm,pt:'Side',sz:m?m[3]:'—',mat:m?m[4]:'—',q:f*q,v:f*v,d:f*d})}\n   if(egSub(r,p.sh)){const pq=egPq(r,p.sh),pv=Math.min(pq,pkv(r,k));if(pq>pv)o.push({...PK,q:pq,v:pv,d:pq-pv})}return}\n  if(d<=0)return;const z=t.z(r,p.sh),sc=t.id=='ab'?'':scOf(r),b={p,t,r,sec:sc};")
# summary / sizes / totals use the number of pockets
rep("pk.map(r=>`<tr>${nmc(r)}<td>1L + 1R${rshT(r,s)}${tg(r)}</td><td>أكريليك</td><td>${+r.q||0}L + ${+r.q||0}R</td>", "pk.map(r=>`<tr>${nmc(r)}<td>1L + 1R${rshT(r,s)}${tg(r)}</td><td>أكريليك</td><td>${egPq(r,s)}L + ${egPq(r,s)}R</td>")
rep("if(pk.length){const n=pk.reduce((a,r)=>a+(+r.q||0),0);", "if(pk.length){const n=pk.reduce((a,r)=>a+egPq(r,s),0);")
rep("if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','1L + 1R','أكريليك',PARTS.eg[1][1]*q);continue}", "if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','1L + 1R','أكريليك',PARTS.eg[1][1]*egPq(r,p.sh));continue}")
rep("pq=rs.filter(r=>egPK(r,s)).reduce((a,r)=>a+(+r.q||0),0);", "pq=rs.filter(r=>egPK(r,s)).reduce((a,r)=>a+egPq(r,s),0);")
# warehouse: the pocket is its own part with its own counters
rep("if(/Acrylic Pocket/.test(z))L.push({ty:'Side Acrylic Pocket',nm:'',sec:'',size:'1L + 1R',mat:'أكريليك',f:PARTS.eg[1][1]})}",
    "if(/Acrylic Pocket/.test(z)){const n=qn(r);L.push({ty:'Side Acrylic Pocket',nm:'',sec:'',size:'1L + 1R',mat:'أكريليك',f:n?PARTS.eg[1][1]*egPq(r,s)/n:0,pk:egSub(r,s)?1:0})}}")
rep("function whSurplus(p){const m={};ckRows(p).forEach(x=>{const r=x.r,d=Math.max(0,(+r.r||0)-(+r.x||0));if(!d)return;whParts(x.t,r,p.sh).forEach(y=>{const k=whKey(y);if(!m[k])m[k]=Object.assign({},y,{q:0});m[k].q=wq(m[k].q+d*y.f)})});return m}",
    "function whSurplus(p){const m={};ckRows(p).forEach(x=>{const r=x.r,d=Math.max(0,(+r.r||0)-(+r.x||0));whParts(x.t,r,p.sh).forEach(y=>{const dd=y.pk?PARTS.eg[1][1]*Math.max(0,pkv(r,'r')-pkv(r,'x')):d*y.f;if(!dd)return;const k=whKey(y);if(!m[k])m[k]=Object.assign({},y,{q:0});m[k].q=wq(m[k].q+dd)})});return m}")
CSS = "\n.tkt tr.tkp td{font-size:.92em}.tkt tr.tkp td:first-child{color:var(--mu);font-weight:800}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'عدد جيوب الأكريليك المطلوب تصنيعها (فاضي = نفس عدد الجندولات)':'Acrylic pockets to make (empty = number of gondolas)'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

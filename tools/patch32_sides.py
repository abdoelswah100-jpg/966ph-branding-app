"""v1.6 fix: acrylic pocket by side, counted in pieces: right (pR) and left (pL), empty = number of gondolas.
Counters rpR/rpL (received), xpR/xpL (executed), wfpR/wfpL (from the warehouse). Old pair counters migrated."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
def cut(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i) + len(b); s = s[:i] + new + s[j:]
assert 'egN=' not in s
cut("const egAO=(r,s)=>egpOf(r,s)===EGPO[2],egSub=", "pkv=(r,k)=>+r[k+'p']||0;",
 "const egAO=(r,s)=>egpOf(r,s)===EGPO[2],egSub=(r,s)=>egPK(r,s),SDS=[['R','يمين'],['L','يسار']],\n egN=(r,s,sd)=>{if(!egPK(r,s))return 0;const v=r['p'+sd];return v!==undefined&&v!==null&&v!==''?Math.max(0,Math.round(+v||0)):(r.q==null?1:(+r.q||0))},egNT=(r,s)=>egN(r,s,'R')+egN(r,s,'L'),pkv=(r,k,sd)=>+r[k+'p'+sd]||0,\n pkZ=(r,q)=>{const c=x=>r[x]!==undefined&&r[x]!==null&&r[x]!=='';if(!c('pR')&&!c('pL'))return '(1L + 1R)';return `(يمين ×${c('pR')?Math.round(+r.pR||0):q} + يسار ×${c('pL')?Math.round(+r.pL||0):q})`};")
cut("function migPK(p){", "p.m16=1}",
 "function migPK(p){if(p.m16b)return;((p.rows||{}).eg||[]).forEach(r=>{if(!egPK(r,p.sh))return;if(r.pq!=null&&r.pq!==''&&r.pR==null){r.pR=r.pL=+r.pq||0}delete r.pq;['r','x'].forEach(k=>{const old=r[k+'p']!=null?+r[k+'p']:(r[k]!=null?+r[k]||0:null);if(old!=null)SDS.forEach(([sd])=>{if(r[k+'p'+sd]==null)r[k+'p'+sd]=Math.min(egN(r,p.sh,sd),old)});delete r[k+'p']});if(r.wfp!=null){SDS.forEach(([sd])=>r['wfp'+sd]=(+r['wfp'+sd]||0)+(+r.wfp||0));delete r.wfp}});p.m16=1;p.m16b=1}")
# fields: right / left in pieces (0 allowed)
rep("Object.assign(num('pq','عدد جيوب الأكريليك المطلوب تصنيعها (فاضي = نفس عدد الجندولات)'),{opt:1,hide:(d,s)=>rsh(d,s)!==2||(EGPO.includes(d.egp)?d.egp:EGPO[0])!==EGPO[0]})",
    "...SDS.map(([sd,n])=>Object.assign(num('p'+sd,'Side Acrylic Pocket '+n+' — عدد القطع (فاضي = عدد الجندولات)'),{opt:1,z0:1,hide:(d,s)=>rsh(d,s)!==2||(EGPO.includes(d.egp)?d.egp:EGPO[0])===EGPO[1]}))")
rep("if(!(v>0)&&!(f.k=='q'&&t.zero&&v==0))", "if(!(v>0)&&!(f.k=='q'&&t.zero&&v==0)&&!(f.z0&&v===0))")
# item text
rep("if(e==EGPO[2])return `${r.nm} · Side Acrylic Pocket (1L + 1R) ×${q}`;", "if(e==EGPO[2]){const pz=pkZ(r,q);return `${r.nm} · Side Acrylic Pocket ${pz}${pz=='(1L + 1R)'?' ×'+q:''}`}")
rep("${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket (1L + 1R)${r.pq!=null&&r.pq!==''&&+r.pq!==+q?' ×'+(+r.pq):''}`:''}", "${s==2&&e!=EGPO[1]?` + Side Acrylic Pocket ${pkZ(r,q)}`:''}")
# totals
rep("pq=rs.filter(r=>egPK(r,s)).reduce((a,r)=>a+egPq(r,s),0);return PARTS.eg.map(([n,f])=>n+' '+f*hq).join(' · ')+(pq?' · Side Acrylic Pocket '+2*pq:'')}",
    "pr=rs.reduce((a,r)=>a+egN(r,s,'R'),0),pl=rs.reduce((a,r)=>a+egN(r,s,'L'),0);return PARTS.eg.map(([n,f])=>n+' '+f*hq).join(' · ')+(pr+pl?` · Side Acrylic Pocket ${pr} يمين + ${pl} يسار`:'')}")
# print summary: right / left / total pieces
cut("if(pk.length){const n=pk.reduce((a,r)=>a+egPq(r,s),0);", "+'</table></div>'}",
 "if(pk.length){const nr=pk.reduce((a,r)=>a+egN(r,s,'R'),0),nl=pk.reduce((a,r)=>a+egN(r,s,'L'),0);tb+=`<h3>Side Acrylic Pocket</h3><div class=\"sc\"><table><tr><th>الجندولة</th><th>يمين</th><th>يسار</th><th>الإجمالي</th><th>الخامة</th><th>ملاحظات</th></tr>`+pk.map(r=>`<tr>${nmc(r)}<td><b>${egN(r,s,'R')}</b></td><td><b>${egN(r,s,'L')}</b></td><td>${egN(r,s,'R')} يمين + ${egN(r,s,'L')} يسار = <b>${egNT(r,s)} قطعة</b>${rshT(r,s)}${tg(r)}</td><td>أكريليك</td><td>${esc(egHS(r,s)?'':r.nt||'')}</td></tr>`).join('')+`<tr class=\"tot\"><td colspan=6><b>إجمالي Side Acrylic Pocket: ${nr} يمين + ${nl} يسار = ${nr+nl} قطعة</b></td></tr>`+'</table></div>'}")
# sizes / management report: right and left rows
rep("if(/Acrylic Pocket/.test(z))k('Side Acrylic Pocket','1L + 1R','أكريليك',PARTS.eg[1][1]*egPq(r,p.sh));continue}", "if(/Acrylic Pocket/.test(z))SDS.forEach(([sd,n])=>{const c=egN(r,p.sh,sd);if(c)k('Side Acrylic Pocket',n,'أكريليك',c)});continue}")
# progress
rep("f=x.t.id=='eg'&&egAO(x.r,x.s)?2:pcs(x.t)", "f=x.t.id=='eg'&&egAO(x.r,x.s)?0:pcs(x.t)")
rep("if(x.t.id=='eg'&&egSub(x.r,x.s)){const pq=egPq(x.r,x.s);n+=2*pq;d+=2*Math.min(pq,pkv(x.r,k))}", "if(x.t.id=='eg'&&egSub(x.r,x.s))SDS.forEach(([sd])=>{const c=egN(x.r,x.s,sd);n+=c;d+=Math.min(c,pkv(x.r,k,sd))})")
# checklist
cut("function tkPk(x,k){", "</div></td></tr>`}",
 "function tkPk(x,k){if(x.t.id!='eg'||!egSub(x.r,x.s))return '';return SDS.map(([sd,n])=>{const q=egN(x.r,x.s,sd);if(!q)return '';const v=pkv(x.r,k,sd),st=v>=q?'ok':v>0?'pt':'no',id=k+'p'+sd+':'+x.t.id+':'+x.i;\n return `<tr class=\"tk-${st} tkp\"><td>↳</td><td>Side Acrylic Pocket - <b>${n}</b> · أكريليك</td><td><b>${q}</b></td><td><div class=\"tkv\"><button class=\"np\" data-tk=\"${id}:-1\" aria-label=\"ناقص\">−</button><input type=\"number\" inputmode=\"numeric\" min=\"0\" data-tv=\"${id}\" value=\"${v}\"><button class=\"np\" data-tk=\"${id}:1\" aria-label=\"زائد\">+</button><button class=\"np tkf\" data-tf=\"${id}\">✓</button></div></td></tr>`}).join('')}")
rep("   return `<tr class=\"tk-${st}\"><td${c?` st", "   if(x.t.id=='eg'&&egAO(x.r,x.s))return `<tr class=\"tk-ao\"><td${c?` style=\"${bgc(c)};font-weight:700\"`:''}>${esc(sc||'—')}</td><td>${esc(dt)}${rshT(x.r,x.s)}</td><td>—</td><td><small>يمين ويسار تحت</small></td></tr>`+tkPk(x,k);\n   return `<tr class=\"tk-${st}\"><td${c?` st")
rep("G.forEach(g=>{const q=g.a.reduce((a,x)=>a+qn(x.r),0),v=g.a.reduce((a,x)=>a+Math.min(qn(x.r),+x.r[k]||0),0);", "G.forEach(g=>{const na=x=>!(x.t.id=='eg'&&egAO(x.r,x.s)),q=g.a.filter(na).reduce((a,x)=>a+qn(x.r),0),v=g.a.filter(na).reduce((a,x)=>a+Math.min(qn(x.r),+x.r[k]||0),0);")
rep("const pk=k.length==2,q=pk?egPq(r,p.sh):qn(r);", "const pk=k.length==3,q=pk?egN(r,p.sh,k[2]):qn(r);")
rep("{const rv=pk?pkv(r,'r'):(+r.r||0);", "{const rv=pk?pkv(r,'r',k[2]):(+r.r||0);")
rep("q=k.length==2?egPq(r,p.sh):qn(r);tkSet(", "q=k.length==3?egN(r,p.sh,k[2]):qn(r);tkSet(")
rep("if(tid=='eg'&&egSub(r,p.sh))r[k+'p']=egPq(r,p.sh)", "if(tid=='eg'&&egSub(r,p.sh))SDS.forEach(([sd])=>r[k+'p'+sd]=egN(r,p.sh,sd))")
rep("if(x.t.id=='eg'&&egSub(x.r,p.sh))x.r[d.tkall+'p']=egPq(x.r,p.sh)", "if(x.t.id=='eg'&&egSub(x.r,p.sh))SDS.forEach(([sd])=>x.r[d.tkall+'p'+sd]=egN(x.r,p.sh,sd))")
rep("if(x.r[d.tkclr+'p']!=null)x.r[d.tkclr+'p']=0", "SDS.forEach(([sd])=>{if(x.r[d.tkclr+'p'+sd]!=null)x.r[d.tkclr+'p'+sd]=0})")
# shortages
rep("PK={...b,nm:r.nm,pt:'Side Acrylic Pocket',sz:'1L + 1R',mat:'أكريليك'};if(egAO(r,p.sh)){if(d>0)o.push({...PK,q,v,d});return}",
    "PK={...b,nm:r.nm,pt:'Side Acrylic Pocket',mat:'أكريليك'},pks=()=>SDS.forEach(([sd,n])=>{const c=egN(r,p.sh,sd),w=Math.min(c,pkv(r,k,sd));if(c>w)o.push({...PK,sz:n,q:c,v:w,d:c-w})});if(egAO(r,p.sh)){pks();return}")
rep("if(egSub(r,p.sh)){const pq=egPq(r,p.sh),pv=Math.min(pq,pkv(r,k));if(pq>pv)o.push({...PK,q:pq,v:pv,d:pq-pv})}return}", "if(egSub(r,p.sh))pks();return}")
rep("const FPX=['ck','nt','r','x','wf','rp','xp','wfp'];", "const FPX=['ck','nt','r','x','wf','rpR','rpL','xpR','xpL','wfpR','wfpL','rp','xp','wfp'];")
rep("if(o0[k+'p']!=null)r[k+'p']=Math.min(+o0[k+'p']||0,egPq(r,p.sh))});['wf','wfp'].forEach", "SDS.forEach(([sd])=>{if(o0[k+'p'+sd]!=null)r[k+'p'+sd]=Math.min(+o0[k+'p'+sd]||0,egN(r,p.sh,sd))})});['wf','wfpR','wfpL'].forEach")
# warehouse
rep("if(/Acrylic Pocket/.test(z)){const n=qn(r);L.push({ty:'Side Acrylic Pocket',nm:'',sec:'',size:'1L + 1R',mat:'أكريليك',f:n?PARTS.eg[1][1]*egPq(r,s)/n:0,pk:egSub(r,s)?1:0})}}",
    "if(/Acrylic Pocket/.test(z)){const n=qn(r);SDS.forEach(([sd,nm2])=>{const c=egN(r,s,sd);if(c)L.push({ty:'Side Acrylic Pocket',nm:'',sec:'',size:nm2,mat:'أكريليك',f:n?c/n:0,pk:sd})})}}")
rep("const dd=y.pk?PARTS.eg[1][1]*Math.max(0,pkv(r,'r')-pkv(r,'x')):d*y.f;", "const dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-pkv(r,'x',y.pk)):d*y.f;")
rep("np=K.length?Math.min(Math.max(0,egPq(r,sh)-(+r.wfp||0)),Math.floor((qty(K[0])+1e-9)/PARTS.eg[1][1])):0;return {M,K,nm,np}}",
    "nps={};K.forEach(y=>{nps[y.pk]=Math.min(Math.max(0,egN(r,sh,y.pk)-(+r['wfp'+y.pk]||0)),Math.floor(qty(y)+1e-9))});const np=K.reduce((a,y)=>a+nps[y.pk],0);return {M,K,nm,np,nps}}")
rep("L.np>0?`${L.np} جيب أكريليك (1L + 1R)`:''", "L.np>0?SDS.filter(([sd])=>(L.nps||{})[sd]>0).map(([sd,n])=>`${L.nps[sd]} جيب ${n}`).join(' + '):''")
rep("if(L.np>0){const x=whFind(whKey(L.K[0]));if(x)whAdd(x,-L.np*PARTS.eg[1][1],'out','ph:'+p.no,note);r.wfp=(+r.wfp||0)+L.np;r.rp=Math.min(egPq(r,p.sh),pkv(r,'r')+L.np)}",
    "L.K.forEach(y=>{const n=(L.nps||{})[y.pk]||0;if(!n)return;const x=whFind(whKey(y));if(x)whAdd(x,-n,'out','ph:'+p.no,note);r['wfp'+y.pk]=(+r['wfp'+y.pk]||0)+n;r['rp'+y.pk]=Math.min(egN(r,p.sh,y.pk),pkv(r,'r',y.pk)+n)});")
cut("c.rows[t.id]=rs.map((r,i)=>{const sub=t.id=='eg'&&egSub(r,c.sh);", "if(pq<=0)r.egp=EGPO[1];else r.pq=pq;r.q=q;return r}",
 "c.rows[t.id]=rs.map((r,i)=>{const sub=t.id=='eg'&&egSub(r,c.sh),ao=sub&&egAO(r,c.sh);let q=ao?0:qn(r)-(+r.wf||0);const pp={};if(sub)SDS.forEach(([sd])=>pp[sd]=egN(r,c.sh,sd)-(+r['wfp'+sd]||0));\n   const L=whRowPlan(t,r,c.sh,st);if(L&&(L.nm>0||L.np>0)){L.M.forEach(y=>st[whKey(y)]=wq((st[whKey(y)]||0)-L.nm*y.f));L.K.forEach(y=>{const n=(L.nps||{})[y.pk]||0;st[whKey(y)]=wq((st[whKey(y)]||0)-n);pp[y.pk]-=n});used.push({tid:t.id,i,n:L.nm,np:L.np,tx:whTxt(L,t),t:t.n,z:t.z(r,c.sh)});q-=L.nm}\n   if(sub){const pr=Math.max(0,pp.R||0),pl=Math.max(0,pp.L||0);if(q<=0&&!pr&&!pl)return null;if(q<=0){r.egp=EGPO[2];r.q=Math.max(1,qn(r));r.pR=pr;r.pL=pl;return r}if(!pr&&!pl){r.egp=EGPO[1];r.q=q;return r}r.q=q;r.pR=pr;r.pL=pl;return r}")
rep("b+Math.min(qn(r),+r.wf||0)+(+r.wfp||0),0),0);", "b+Math.min(qn(r),+r.wf||0)+(+r.wfpR||0)+(+r.wfpL||0),0),0);")
rep("Old Turkish: needed = full (header + side + Side Acrylic Pocket 1L + 1R) / backlight + sticker only / acrylic only; the pocket is its own line", "Old Turkish: needed = full (header + side + Side Acrylic Pocket right + left) / backlight + sticker only / acrylic only; pockets right and left counted in pieces (empty = number of gondolas), each its own line")
rep("'Old Turkish gondola: number of acrylic pockets to make; the pocket has its own received / executed counter under each gondola,", "'Old Turkish gondola: acrylic pockets right and left in pieces (empty = number of gondolas); each side has its own received / executed counter under each gondola,")
assert 'egPq' not in s, [s[m-60:m+60] for m in [s.find('egPq')]]
CSS = "\n.tkt tr.tk-ao td{background:var(--c)}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'Side Acrylic Pocket يمين — عدد القطع (فاضي = عدد الجندولات)':'Side Acrylic Pocket right — pieces (empty = number of gondolas)','Side Acrylic Pocket يسار — عدد القطع (فاضي = عدد الجندولات)':'Side Acrylic Pocket left — pieces (empty = number of gondolas)','يمين':'Right','يسار':'Left','يمين ويسار تحت':'Right and left below','جيب يمين':'right pocket','جيب يسار':'left pocket'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)
